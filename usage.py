"""Read-only functions used by App-Manager: program usage, startup entries, winget and duplicates."""
import codecs, datetime, os, re, struct, subprocess
from pathlib import Path

from i18n import tr

NOWIN = 0x08000000
UA_BASE = r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"


def _known():
    e = os.environ.get
    home, pd, ad = e("USERPROFILE", ""), e("ProgramData", ""), e("APPDATA", "")
    win = e("SystemRoot", r"C:\Windows")
    sm = r"\Microsoft\Windows\Start Menu\Programs"
    return {
        "6D809377-6AF0-444B-8957-A3773F02200E": e("ProgramW6432", e("ProgramFiles", "")),
        "7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E": e("ProgramFiles(x86)", ""),
        "905E63B6-C1BF-494E-B29C-65B732D3D21A": e("ProgramFiles", ""),
        "1AC14E77-02E7-4E5D-B744-2EB1AE5198B7": win + r"\System32",
        "D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27": win + r"\SysWOW64",
        "F38BF404-1D43-42F2-9305-67DE0B28FC23": win,
        "0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8": pd + sm,
        "A77F5D77-2E2B-44C3-A6A2-ABA601054A51": ad + sm,
        "B4BFCC3A-DB2C-424C-B029-7FE99A87C641": home + r"\Desktop",
        "374DE290-123F-4565-9164-39C4925E467B": home + r"\Downloads",
        "FDD39AD0-238F-46AF-ADB4-6C85480369C7": home + r"\Documents",
        "F1B32785-6FBA-4FCF-9D55-7B8E7F157091": e("LOCALAPPDATA", ""),
        "3EB685DB-65F9-4CF6-A03A-E3EF65729F3D": ad,
        "DFDF76A2-C82A-4D63-906A-5644AC457385": e("PUBLIC", ""),
        "5E6C858F-0E22-4760-9AFE-EA3317B67173": home,
        "9E3995AB-1F9C-4F13-B827-48B24B6C7174": ad + r"\Microsoft\Internet Explorer\Quick Launch\User Pinned",
        "C4AA340D-F20F-4863-AFEF-F87EF2E6BA25": e("PUBLIC", "") + r"\Desktop",
        "62AB5D82-FDC1-4DC3-A9DD-070D1D495D97": pd,
    }


def _expand(path, known):
    m = re.match(r"^\{([0-9A-Fa-f-]{36})\}[\\/]?(.*)$", path)
    if m and m.group(1).upper() in known:
        return os.path.join(known[m.group(1).upper()], m.group(2))
    return path


def userassist():
    """{lowercase_path: (times, last_use_datetime|None)} read from the registry (UserAssist, read-only)."""
    import winreg
    known, out = _known(), {}
    try:
        base = winreg.OpenKey(winreg.HKEY_CURRENT_USER, UA_BASE)
    except OSError:
        return out
    for gi in range(winreg.QueryInfoKey(base)[0]):
        try:
            cnt = winreg.OpenKey(base, winreg.EnumKey(base, gi) + r"\Count")
        except OSError:
            continue
        for vi in range(winreg.QueryInfoKey(cnt)[1]):
            try:
                name, data, _ = winreg.EnumValue(cnt, vi)
            except OSError:
                continue
            if len(data) < 68 or name.startswith("UEME_"):
                continue
            n = struct.unpack_from("<I", data, 4)[0]
            ft = struct.unpack_from("<Q", data, 60)[0]
            when = None
            if ft:
                try:
                    when = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ft / 10)
                    when = when.replace(tzinfo=datetime.timezone.utc).astimezone().replace(tzinfo=None)
                except (OverflowError, ValueError):
                    when = None
            key = os.path.normpath(_expand(codecs.decode(name, "rot13"), known)).lower()
            o = out.get(key)
            out[key] = (max(n, o[0]) if o else n, max([t for t in (when, o and o[1]) if t], default=None))
    return out


def usage_index(ua):
    """Extra index by .lnk file name (to match when the shortcut path differs)."""
    by = {}
    for k, v in ua.items():
        if k.endswith(".lnk"):
            b = os.path.basename(k)
            o = by.get(b)
            by[b] = (max(v[0], o[0]) if o else v[0], max([t for t in (v[1], o and o[1]) if t], default=None))
    return by


def usage_of(item, ua, by_lnk):
    """(times, last_use) from Windows for an index item; (0, None) if there is no record."""
    found = []
    for k in (item.get("target"), item.get("lnk")):
        if k and os.path.normpath(k).lower() in ua:
            found.append(ua[os.path.normpath(k).lower()])
    if not found and item.get("lnk"):
        v = by_lnk.get(os.path.basename(item["lnk"]).lower())
        if v:
            found.append(v)
    if not found:
        return 0, None
    return max(f[0] for f in found), max([f[1] for f in found if f[1]], default=None)


# ---------- startup with Windows ----------
RUN_KEYS = [("HKCU", r"Software\Microsoft\Windows\CurrentVersion\Run", "Run (usuário)"),
            ("HKLM", r"Software\Microsoft\Windows\CurrentVersion\Run", "Run (todos)"),
            ("HKLM", r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "Run (todos, 32 bits)")]


def _exe_of(cmd):
    cmd = os.path.expandvars(cmd or "").strip()
    m = re.match(r'^"([^"]+)"', cmd) or re.match(r"^(.*?\.exe)\b", cmd, re.I)
    return os.path.normpath(m.group(1)).lower() if m else ""


def startup_entries():
    """List of {'exe','nome','onde','ativo'} for programs that start with Windows (registry + Startup folder)."""
    import winreg
    out = []
    for hive, sub, onde in RUN_KEYS:
        root = winreg.HKEY_CURRENT_USER if hive == "HKCU" else winreg.HKEY_LOCAL_MACHINE
        appr = {}
        try:
            ak = winreg.OpenKey(root, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run")
            for i in range(winreg.QueryInfoKey(ak)[1]):
                n, d, _ = winreg.EnumValue(ak, i)
                appr[n] = not (d and d[0] & 1)       # 02/06 = enabled, 03/07 = disabled by the user
        except OSError:
            pass
        try:
            k = winreg.OpenKey(root, sub)
        except OSError:
            continue
        for i in range(winreg.QueryInfoKey(k)[1]):
            try:
                n, v, _ = winreg.EnumValue(k, i)
            except OSError:
                continue
            out.append({"exe": _exe_of(str(v)), "nome": n, "onde": onde, "ativo": appr.get(n, True)})
    for base, onde in ((os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"), "Pasta Inicializar (usuário)"),
                       (os.path.join(os.environ.get("ProgramData", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"), "Pasta Inicializar (todos)")):
        if os.path.isdir(base):
            for f in os.listdir(base):
                if f.lower().endswith(".lnk"):
                    out.append({"exe": "", "nome": Path(f).stem, "onde": onde, "ativo": True})
    return out


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def startup_of(item, entries):
    """Startup entry matching the item, or None."""
    tgt = os.path.normpath(item.get("target") or "").lower() if item.get("target") else ""
    loc = (item.get("location") or "").lower().rstrip("\\")
    n = norm(item["name"])
    for e in entries:
        if tgt and e["exe"] == tgt:
            return e
    win = os.environ.get("SystemRoot", r"C:\Windows").lower()
    if loc and not loc.startswith(win) and len(Path(loc).parts) >= 3 and not item.get("launcher"):
        for e in entries:
            if e["exe"] and e["exe"].startswith(loc + "\\"):
                return e
    for e in entries:
        en = norm(e["nome"])
        if not e["exe"] and en and en == n:
            return e
    return None


# ---------- updates (winget) ----------
def winget_upgrades(timeout=180):
    """Run `winget upgrade` (list only) and return [{'nome','id','atual','nova'}]. Raises OSError if winget is missing."""
    r = subprocess.run(["winget", "upgrade", "--accept-source-agreements", "--disable-interactivity"],
                       capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout, creationflags=NOWIN)
    return parse_winget(r.stdout.decode("utf-8", errors="replace"))


def parse_winget(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    for n in range(1, len(lines)):
        if re.fullmatch(r"-{8,}\s*", lines[n].strip() or "x"):
            head = lines[n - 1]
            starts = [m.start() for m in re.finditer(r"\S+(?: \S+)*", head)]
            if len(starts) < 4:
                continue
            res = []
            for ln in lines[n + 1:]:
                if not ln.strip():
                    break
                cols = [ln[a:b].strip() for a, b in zip(starts, starts[1:] + [len(ln) + 1])]
                if len(cols) >= 4 and cols[1] and cols[3] and " " not in cols[1]:
                    res.append({"nome": cols[0], "id": cols[1], "atual": cols[2], "nova": cols[3],
                                "origem": cols[4] if len(cols) > 4 else ""})
            return res
    return []


def match_updates(items, ups):
    """{item_name: {'id','atual','nova'}} matching the winget name against the item or the registry name."""
    out = {}
    for it in items:
        if it.get("broken") or it.get("launcher") or it.get("manual"):
            continue
        keys = {norm(it["name"]), norm(it.get("uninstall_nome") or "")} - {""}
        for u in ups:
            un = norm(u["nome"])
            if u.get("origem", "").lower() == "msstore":      # Store apps are not in this index
                continue
            if un and any(k == un or (min(len(k), len(un)) >= 8 and min(len(k), len(un)) / max(len(k), len(un)) >= 0.55
                                                         and (k.startswith(un) or un.startswith(k))) for k in keys):
                out[it["name"]] = {"id": u["id"], "atual": u["atual"], "nova": u["nova"]}
                break
    return out


# ---------- duplicate versions ----------
def dup_base(name):
    s = name.lower()
    s = re.sub(r"\((?:x64|x86|64-bit|32-bit)[^)]*\)|\b(x64|x86|64-bit|32-bit)\b", " ", s)
    s = re.sub(r"\bv?\d+(?:[.\-_]\d+)*\b", " ", s)
    s = re.sub(r"[()\[\]]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def dup_groups(items):
    """{base: [items]} only for groups with 2+ different names within the same category."""
    g = {}
    for i in items:
        if i.get("broken") or i.get("launcher") or i.get("manual"):
            continue
        b = dup_base(i["name"])
        if len(b) >= 3:
            g.setdefault((i["category"], b), []).append(i)
    return {f"{b}": v for (c, b), v in g.items() if len({norm(x["name"]) for x in v}) >= 2}


# ---------- dates ----------
def rel_days(dt, now=None):
    now = now or datetime.datetime.now()
    d = (now.date() - dt.date()).days
    if d <= 0: return tr("hoje")
    if d == 1: return tr("ontem")
    if d < 30: return tr("há {n} dias", n=d)
    if d < 365: return tr("há {n} mês(es)", n=d // 30)
    return tr("há {n} ano(s)", n=d // 365)
