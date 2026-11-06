"""Varre atalhos do Menu Iniciar + registro do Windows e gera index.json (somente leitura).

Fase 1: grava a lista rapidamente (tamanhos = null, "sizing": true).
Fase 2: calcula os tamanhos em seguida, regravando o arquivo aos poucos.
"""
import hashlib, json, os, re, subprocess, tempfile, time
from pathlib import Path

import config
from paths import APP as BASE

IDX, ICONS = BASE / "index.json", BASE / "icons"
NOWIN = 0x08000000

PS_MAIN = r'''
$ErrorActionPreference='SilentlyContinue'
$roots=@("$env:ProgramData\Microsoft\Windows\Start Menu\Programs","$env:APPDATA\Microsoft\Windows\Start Menu\Programs")
$sh=New-Object -ComObject WScript.Shell
$lnks=foreach($f in Get-ChildItem $roots -Recurse -Filter *.lnk){
  $l=$sh.CreateShortcut($f.FullName); $t=$l.TargetPath; $v=$null
  if($t -and (Test-Path -LiteralPath $t -PathType Leaf)){ $v=(Get-Item -LiteralPath $t).VersionInfo }
  [pscustomobject]@{lnk=$f.FullName;name=$f.BaseName;target=$t;args=$l.Arguments;
    ver=$(if($v){if($v.ProductVersion){$v.ProductVersion}else{$v.FileVersion}});
    desc=$v.FileDescription;company=$v.CompanyName;product=$v.ProductName}
}
$keys='HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
$reg=foreach($k in $keys){ Get-ItemProperty $k | Where-Object {$_.DisplayName -and -not $_.SystemComponent -and -not $_.ParentKeyName} |
  Select-Object DisplayName,DisplayVersion,Publisher,InstallLocation,DisplayIcon,EstimatedSize,UninstallString,InstallDate,@{n='Key';e={$_.PSChildName}} }
@{lnks=@($lnks);reg=@($reg)} | ConvertTo-Json -Depth 4 -Compress | Out-File -Encoding utf8 -LiteralPath $env:SCAN_OUT
'''
PS_ICONS = r'''
$ErrorActionPreference='SilentlyContinue'
Add-Type -AssemblyName System.Drawing
foreach($line in Get-Content -LiteralPath $env:ICON_IN -Encoding UTF8){
  $h,$t=$line -split '\|',2; $o=Join-Path $env:ICON_DIR "$h.png"
  if(Test-Path -LiteralPath $o){continue}
  try{ $i=[System.Drawing.Icon]::ExtractAssociatedIcon($t)
    if($i){ $b=$i.ToBitmap(); $s=New-Object System.Drawing.Bitmap 16,16
      $g=[System.Drawing.Graphics]::FromImage($s); $g.InterpolationMode='HighQualityBicubic'
      $g.DrawImage($b,0,0,16,16); $s.Save($o,[System.Drawing.Imaging.ImageFormat]::Png) } }catch{}
}
'''
SKIP = re.compile(r"uninstall|desinstal|readme|leia-?me|\bhelp\b|ajuda|license agreement|release notes|"
                  r"documenta|manual|website|visit |changelog|eula", re.I)
SKIP_EXE = re.compile(r"unins|uninst|setup\.exe$|installer", re.I)
REG_JUNK = re.compile(r"redistributable|runtime|update for|hotfix|\bkb\d|driver|windows software development|"
                      r"language pack|\.net |webview2|visual c\+\+|microsoft edge update|vcredist|sdk|"
                      r"component|package|\bpatch\b|proofing|bootstrapper|helper|plugin|plug-in|chipset|openal|adobe air", re.I)
GENERIC = re.compile(r"^[a-z]:\\(windows|programdata)(\\|$)", re.I)
LOCAL = os.environ.get("LOCALAPPDATA", "").lower()
ROOTS = [r for r in (os.environ.get("ProgramFiles", "").lower(), os.environ.get("ProgramFiles(x86)", "").lower(), LOCAL) if r]
_cache = {}


def run_ps(script, env):
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8-sig") as t:
        t.write(script)
    try:
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", t.name],
                       capture_output=True, stdin=subprocess.DEVNULL, env={**os.environ, **env}, creationflags=NOWIN)
    finally:
        os.unlink(t.name)


def icon_key(target):
    return hashlib.sha1(target.lower().encode("utf-8")).hexdigest()[:16]


def install_root(exe):
    low = exe.lower()
    for r in ROOTS:
        if low.startswith(r + "\\"):
            parts = Path(exe).relative_to(Path(exe).anchor).parts
            n = len(Path(r).relative_to(Path(r).anchor).parts)
            sub = parts[: n + 1]
            if r == LOCAL and len(parts) > n + 1 and parts[n].lower() == "programs":
                sub = parts[: n + 2]
            return str(Path(Path(exe).anchor, *sub))
    return str(Path(exe).parent)


def dir_size(p):
    if p in _cache:
        return _cache[p]
    total = 0
    for dp, _, fs in os.walk(p, onerror=lambda e: None):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass
    _cache[p] = total
    return total


def catalog_hit(item, cfg):
    """Primeira entrada do catálogo cujo termo aparece no NOME (prefixo '=' = nome exato)."""
    nm = item["name"].lower()
    for e in cfg.get("catalogo", []):
        for k in e["k"]:
            if (nm == k[1:]) if k.startswith("=") else (k in nm):
                return e
    return None


def purpose_of(item, cfg):
    d = cfg.get("descricoes", {}).get(item["name"])
    if d:
        return d
    e = catalog_hit(item, cfg)
    if e and e.get("d"):
        return e["d"]
    return item.get("desc") or item.get("product") or ""


def categorize(item, cfg):
    """Devolve (categoria, subcategoria)."""
    over = cfg.get("overrides", {}).get(item["name"])
    if over:
        c, _, s = over.partition(" > ")
        return c.strip(), (s.strip() or "Geral")
    e = catalog_hit(item, cfg)
    if e:
        return e["c"], e.get("s") or "Geral"
    hay = " ".join([item["name"], item.get("company") or "", item.get("product") or ""]).lower()
    for cat, words in cfg["regras"].items():
        if any(w.lower() in hay for w in words):
            return cat, "Geral"
    return "Outros", "Geral"


# ---------- programas que abrem por .bat/.cmd (portáteis, sem instalador) ----------
LAUNCH = re.compile(r"(^|[^a-z0-9])(run|start|launch|launcher|iniciar|abrir|open|play|webui|server|gui|main|app)([^a-z0-9]|$)", re.I)
GENERIC_STEM = re.compile(r"(run|start|launch|launcher|iniciar|abrir|open|play|webui|server|gui|main|app)([ _-].*)?", re.I)
LAUNCH_EXCL = re.compile(r"(un)?install|setup|activate|conda|(^|[^a-z])(npm|npx|node|dart|bun|yarn)([^a-z]|$)|^pre_|^post_|"
                         r"gradlew|^script|test|build|apply|check|clone|stub|hook|format|sign|^d8|driver|update", re.I)
LAUNCH_SKIPDIRS = {"venv", ".venv", "env", "node_modules", ".git", "python_embeded", "python_embedded", "__pycache__",
                   "site-packages", "lib", "library", "pkgs", "bin", "shims", "condabin", "internal", "tests", "test",
                   "fixtures", "docs", "examples", "prototype", "drivers", "build-tools", "platform-tools", "cache",
                   "tmpdir", "$recycle.bin", "windows", "program files", "program files (x86)", "programdata", "appdata",
                   "system volume information", "android_sdk", "firmwares & postconfiguration"}
LOOSE_DIRS = {"downloads", "desktop", "documents", "documentos", "área de trabalho", "temp", "tmp"}
BAT_SKIPLINE =re.compile(r"^(@?echo\b|rem\b|::|setlocal|endlocal|cd\b|pushd|popd|title\b|chcp|cls\b|color\b|set\b|pause|exit\b|goto\b|:)", re.I)


def fixed_drives():
    import ctypes
    out, mask = [], ctypes.windll.kernel32.GetLogicalDrives()
    for n in range(26):
        d = f"{chr(65 + n)}:\\"
        if mask >> n & 1 and ctypes.windll.kernel32.GetDriveTypeW(d) == 3:
            out.append(d)
    return out


def launcher_roots(cfg):
    home = Path.home()
    roots = [(home / "Downloads", 3, True), (home / "Desktop", 4, True), (home / "Documents", 3, True)]
    sysdrv = os.environ.get("SystemDrive", "C:").upper() + "\\"
    roots += [(Path(d), 3, True) for d in fixed_drives() if d.upper() != sysdrv]
    roots += [(Path(x), 3, False) for x in cfg.get("launchers", {}).get("raizes_extra", [])]
    return roots


def pretty(s):
    return re.sub(r"\s+", " ", s.replace("_", " ")).strip()


def bat_command(path):
    try:
        for ln in Path(path).read_text(encoding="utf-8", errors="replace").splitlines()[:60]:
            ln = ln.strip().lstrip("@")
            if ln and not BAT_SKIPLINE.match(ln):
                return ln[:110]
    except OSError:
        pass
    return ""


def find_launchers(cfg, skip_locs, self_dir):
    """Pastas com .bat/.cmd de inicialização (ex.: run.bat) -> lista de itens (um por pasta)."""
    seen, groups = set(), {}
    for root, maxd, only_strong_at_top in launcher_roots(cfg):
        if not root.is_dir():
            continue
        for dp, dn, fn in os.walk(str(root), onerror=lambda e: None):
            try:
                depth = len(Path(dp).relative_to(root).parts)
            except ValueError:
                continue
            low = dp.lower()
            if low.startswith(self_dir) or any(low == l or low.startswith(l + "\\") for l in skip_locs):
                dn[:] = []
                continue
            dn[:] = [d for d in dn if d.lower() not in LAUNCH_SKIPDIRS and not d.startswith(".")] if depth < maxd else []
            cand = [f for f in fn if f.lower().endswith((".bat", ".cmd")) and not LAUNCH_EXCL.search(Path(f).stem)]
            strong = [f for f in cand if LAUNCH.search(Path(f).stem)]
            loose = depth == 0 or Path(dp).name.lower() in LOOSE_DIRS      # pasta "solta": não é a pasta de um programa
            pick = strong or (cand if len(cand) == 1 and not loose else [])
            pick = [f for f in pick if os.path.realpath(os.path.join(dp, f)).lower() not in seen]
            if not pick:
                continue
            for f in pick:
                seen.add(os.path.realpath(os.path.join(dp, f)).lower())
            pick.sort(key=lambda f: (bool(re.search(r"c[oó]pia|copy", f, re.I)), f.lower()))
            groups[dp] = (pick, loose)
    out = []
    for dp, (files, at_root) in groups.items():
        stem = Path(files[0]).stem
        if len(files) == 1 and not GENERIC_STEM.fullmatch(stem) or at_root:
            name = pretty(stem)
        else:
            name = pretty(Path(dp).name)
        main = os.path.join(dp, files[0])
        cmd = bat_command(main)
        out.append({"lnk": "", "name": name, "target": main, "ver": "", "company": "", "product": "", "desc": "",
                    "launcher": True, "variants": [os.path.join(dp, f) for f in files], "location": dp,
                    "size": os.path.getsize(main) if at_root else None, "_root": None if at_root else dp,
                    "_cmd": cmd})
    return out


def find_uninstall(item, reg_info):
    """Acha a entrada de desinstalação do registro que corresponde ao item (ou None)."""
    tgt = (item.get("target") or "").lower()
    if not tgt or tgt.startswith("c:\\windows"):
        return None
    n = norm(item["name"])
    # 1) pelo nome (igual ou um começa com o outro)
    for r in reg_info:
        if n and r["n"] and (n == r["n"] or (min(len(n), len(r["n"])) >= 5 and min(len(n), len(r["n"])) / max(len(n), len(r["n"])) >= 0.55
                                             and (r["n"].startswith(n) or n.startswith(r["n"])))):
            return r
    # 2) pelo executável, só se for exclusivo daquela entrada
    same = [r for r in reg_info if r["exe"] and r["exe"] == tgt]
    if len(same) == 1:
        return same[0]
    # 3) pela pasta de instalação (a mais específica)
    inside = [r for r in reg_info if r["loc"] and tgt.startswith(r["loc"] + "\\")]
    return max(inside, key=lambda r: len(r["loc"])) if inside else None


def install_date(item):
    """Data de criação da pasta de instalação (ou do executável): aproxima a data de instalação."""
    for p in (item.get("location"), item.get("target")):
        try:
            if p and os.path.exists(p):
                return time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(p)))
        except OSError:
            pass
    return ""


def uninstall_cmd(s):
    s = (s or "").strip()
    return re.sub(r"(?i)(msiexec(?:\.exe)?\s+)/I(\s*\{)", r"\1/X\2", s)


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def save(items, removed, sizing):
    data = {"gerado": time.strftime("%Y-%m-%d %H:%M"), "sizing": sizing, "removidos": removed, "items": items}
    tmp = IDX.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, IDX)


def main():
    cfg = config.load()
    prev = {}
    if IDX.exists():
        try:
            old = json.loads(IDX.read_text(encoding="utf-8"))
            prev = {i["name"]: i for i in (old.get("items", []) if isinstance(old, dict) else old)}
        except (OSError, ValueError):
            pass

    out = Path(tempfile.gettempdir()) / "appmanager_scan_out.json"
    out.unlink(missing_ok=True)
    run_ps(PS_MAIN, {"SCAN_OUT": str(out)})
    try:
        raw = json.loads(out.read_text(encoding="utf-8-sig"))
        out.unlink()
    except (OSError, ValueError):
        raw = {}
    lnks, reg = raw.get("lnks") or [], raw.get("reg") or []

    items, seen = [], set()
    for x in lnks:
        tgt = x.get("target") or ""
        if SKIP.search(x["name"]) or not tgt.lower().endswith(".exe"):
            continue
        if SKIP_EXE.search(os.path.basename(tgt)):
            continue
        if not os.path.isfile(tgt):               # atalho quebrado
            x.update(location=str(Path(tgt).parent), size=0, broken=True)
            x["category"], x["sub"] = "Atalhos quebrados", categorize(x, cfg)[0]
            x["purpose"] = ("Atalho quebrado: o programa de destino não existe mais (provavelmente foi desinstalado). "
                            + purpose_of(x, cfg)).strip()
            items.append(x)
            continue
        key = tgt.lower() + "|" + (x.get("args") or "")
        if key in seen:
            continue
        seen.add(key)
        root = install_root(tgt)
        if GENERIC.match(tgt):
            x.update(location=str(Path(tgt).parent), size=os.path.getsize(tgt), _root=None)
        else:
            x.update(location=root, size=None, _root=root)
        x["purpose"] = purpose_of(x, cfg)
        x["category"], x["sub"] = categorize(x, cfg)
        items.append(x)

    # programas instalados sem atalho no Menu Iniciar (registro do Windows)
    have = [norm(i["name"]) for i in items if not i.get("broken")]
    locs = [i["location"].lower() for i in items if i.get("location")]
    def _exe(r):
        ico = (r.get("DisplayIcon") or "").strip().strip('"').split(",")[0].strip('"')
        return ico.lower() if ico.lower().endswith(".exe") else ""
    shared = {}
    for r in reg:
        shared[_exe(r)] = shared.get(_exe(r), 0) + 1
    known = {i["target"].lower() for i in items if i.get("target")}
    for r in reg:
        nm = r.get("DisplayName") or ""
        e = _exe(r)
        if e in known or shared.get(e, 0) >= 3 or GENERIC.match(e):     # mesmo exe de outro item / pacote de bibliotecas
            continue
        n = norm(nm)
        if not n or REG_JUNK.search(nm) or any(n in h or h in n for h in have if len(h) > 3):
            continue
        il = (r.get("InstallLocation") or "").strip().strip('"')
        if il and any(l.startswith(il.lower().rstrip("\\")) for l in locs):
            continue
        ico = (r.get("DisplayIcon") or "").strip().strip('"').split(",")[0].strip('"')
        exe = ico if ico.lower().endswith(".exe") and os.path.isfile(ico) else ""
        if exe and SKIP_EXE.search(os.path.basename(exe)):
            exe = ""
        if not exe or SKIP.search(nm):      # sem executável abrível = biblioteca/driver, ignora
            continue
        loc = il if il and os.path.isdir(il) else str(Path(exe).parent)
        it = {"lnk": "", "name": nm, "target": exe, "ver": r.get("DisplayVersion") or "",
              "company": r.get("Publisher") or "", "product": nm, "desc": "", "sematalho": True,
              "location": loc, "size": (int(r["EstimatedSize"]) * 1024 if r.get("EstimatedSize") else None),
              "_root": loc if loc and not GENERIC.match(loc) and r.get("EstimatedSize") is None else None}
        it["purpose"] = purpose_of(it, cfg)
        it["category"], it["sub"] = categorize(it, cfg)
        items.append(it)

    # programas que abrem por .bat/.cmd (sem atalho nem instalador)
    skip_locs = {i["location"].lower().rstrip("\\") for i in items
                 if i.get("location") and not GENERIC.match(i["location"]) and len(Path(i["location"]).parts) >= 2}
    have = {norm(i["name"]) for i in items}
    for L in find_launchers(cfg, skip_locs, str(BASE).lower()):
        if norm(L["name"]) in have:
            continue
        have.add(norm(L["name"]))
        hit = catalog_hit(L, cfg)
        cmd = L.pop("_cmd")
        L["purpose"] = purpose_of(L, cfg) if hit else (
            f"Programa aberto por script ({Path(L['target']).name})" + (f"; primeiro comando: {cmd}" if cmd else "") + ".")
        if hit or L["name"] in cfg.get("overrides", {}):
            L["category"], L["sub"] = categorize(L, cfg)
        else:
            L["category"], L["sub"] = "Programas sem instalador", "Scripts (.bat/.cmd)"
        items.append(L)

    # desinstalador (do registro do Windows) de cada item
    reg_info = []
    for r in reg:
        cmd = uninstall_cmd(r.get("UninstallString"))
        # ignora desinstaladores que só apagam arquivos (cmd /c del) ou abrem outro app (steam://)
        if not cmd or re.search(r"(?i)^cmd(\.exe)?\s+/c\s+del\b|steam://", cmd):
            continue
        il = (r.get("InstallLocation") or "").strip().strip('"').rstrip("\\").lower()
        d = str(r.get("InstallDate") or "")
        reg_info.append({"n": norm(r.get("DisplayName") or ""), "exe": _exe(r), "cmd": cmd, "nome": r.get("DisplayName") or "",
                         "data": f"{d[:4]}-{d[4:6]}-{d[6:8]}" if re.fullmatch(r"20\d{6}|19\d{6}", d) else "",
                         "loc": il if il and not GENERIC.match(il) and len(il) > 6 else ""})
    for i in items:
        u = None if (i.get("broken") or i.get("launcher")) else find_uninstall(i, reg_info)
        if u:
            i["uninstall"], i["uninstall_nome"] = u["cmd"], u["nome"]
        i["instalado"] = (u and u["data"]) or install_date(i)

    # novos / removidos desde o último scan
    cur = {i["name"] for i in items}
    for i in items:
        if prev and i["name"] not in prev:
            i["novo"] = True
    removed = sorted(n for n in prev if n not in cur and not prev[n].get("broken")) if prev else []

    # ícones
    ICONS.mkdir(exist_ok=True)
    lines = [f"{icon_key(i['target'])}|{i['target']}" for i in items if i.get("target") and os.path.isfile(i["target"])]
    if lines:
        inp = Path(tempfile.gettempdir()) / "appmanager_icons_in.txt"
        inp.write_text("\n".join(lines), encoding="utf-8-sig")
        run_ps(PS_ICONS, {"ICON_IN": str(inp), "ICON_DIR": str(ICONS)})
        inp.unlink(missing_ok=True)

    items.sort(key=lambda i: (i["category"], i.get("sub", ""), i["name"].lower()))
    pend = [i for i in items if i.get("_root")]
    # reaproveita tamanhos antigos enquanto calcula
    for i in pend:
        i["size"] = prev.get(i["name"], {}).get("size")
    save([{k: v for k, v in i.items() if k != "_root"} for i in items], removed, bool(pend))
    print(f"{len(items)} itens (de {len(lnks)} atalhos); calculando tamanhos…", flush=True)

    # fase 2: tamanhos
    for n, i in enumerate(pend, 1):
        i["size"] = dir_size(i["_root"])
        if n % 15 == 0 and n < len(pend):
            save([{k: v for k, v in j.items() if k != "_root"} for j in items], removed, True)
    save([{k: v for k, v in j.items() if k != "_root"} for j in items], removed, False)
    print("pronto", flush=True)


if __name__ == "__main__":
    main()
