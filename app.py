import csv, datetime, html, hashlib, json, os, re, shutil, subprocess, sys, tempfile, threading, time, unicodedata, webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path

import config
import usage
from i18n import tr, trc, trd, LANG, LANGS
from paths import APP as BASE, RES
from version import APP_NAME, VERSION, REPO_URL

UPD = BASE / "updates.json"                   # cache of the last winget check
BACKUPS = BASE / "backup"                     # configuration backups
COLS = {"versao": (tr("Versão"), 90), "upd": (tr("Atualização"), 105), "tamanho": (tr("Tamanho"), 75), "disco": (tr("Disco"), 45),
        "ultimo": (tr("Último uso"), 190), "vezes": (tr("Vezes usado"), 90), "instalado": (tr("Instalado em"), 95),
        "inicia": (tr("Inicia com Windows"), 140), "tags": (tr("Tags"), 100), "cat": (tr("Categoria › Subcategoria"), 200),
        "local": (tr("Local"), 300)}
DEFAULT_COLS = ["versao", "upd", "tamanho", "disco", "ultimo", "vezes", "instalado", "inicia", "cat", "local"]
KEEP = ("favoritos", "usos", "ultimo", "descricoes", "notas", "tags", "ocultos", "manuais", "colunas")
IDX, USR, ICONS = BASE / "index.json", BASE / "user.json", BASE / "icons"
HELP = RES / "help" / f"{LANG}.md"             # text of the Help window (keep it up to date: see CLAUDE.md)
if not HELP.exists():
    HELP = RES / "help" / "pt.md"
BACKUP = BASE / "backup" / "atalhos"          # copies of shortcuts sent to the Recycle Bin (so they can be undone)
NOWIN = 0x08000000
MB = 1024 * 1024
LIGHT = dict(bg="#f3f3f3", fg="#1b1b1b", field="#ffffff", sel="#cfe3ff", selfg="#000000", head="#e0e0e0", link="#0b57d0")
DARK = dict(bg="#1f1f23", fg="#e6e6e6", field="#2a2a2f", sel="#2f5d9e", selfg="#ffffff", head="#3a3a41", link="#7ab0ff")
VIRTUAL = [("__all__", tr("Todos")), ("__fav__", tr("★ Favoritos")), ("__top__", tr("Mais usados")),
           ("__new__", tr("Novos desde o último scan")), ("__nolnk__", tr("Sem atalho no Menu Iniciar")),
           ("__old__", tr("Sugestão de limpeza (sem uso)")), ("__start__", tr("Iniciam com o Windows")),
           ("__upd__", tr("Com atualização (winget)")), ("__dup__", tr("Versões duplicadas"))]
ALL_DISKS, ANY_SIZE = tr("Todos os discos"), tr("Qualquer tamanho")
SIZES = {ANY_SIZE: None,
         tr("Menor que 100 MB"): lambda s: s is not None and s < 100 * MB,
         tr("Maior que 100 MB"): lambda s: s is not None and s > 100 * MB,
         tr("Maior que 500 MB"): lambda s: s is not None and s > 500 * MB,
         tr("Maior que 1 GB"): lambda s: s is not None and s > 1024 * MB,
         tr("Maior que 5 GB"): lambda s: s is not None and s > 5 * 1024 * MB}
HIST_MAX = 300
BACKUP_FORMAT = "app-manager-backup-1"


def fmt(n):
    if n is None:
        return "…"
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024


def system_dark():
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        return winreg.QueryValueEx(k, "AppsUseLightTheme")[0] == 0
    except OSError:
        return False


def read_json(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


def write_json(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", slug(s))


def fmt_date(s):
    if not s or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return ""
    try:
        return datetime.date(int(s[:4]), int(s[5:7]), int(s[8:10])).strftime(tr("%d/%m/%Y"))
    except ValueError:                             # invalid date in the Windows registry
        return f"{s[8:10]}/{s[5:7]}/{s[:4]}"


def disk_of(i):
    m = re.match(r"^([a-zA-Z]):", i.get("location") or i.get("target") or "")
    return m.group(1).upper() + ":" if m else "—"


def self_env():
    """Environment for relaunching the .exe itself (PyInstaller): the child must extract its own files."""
    return {**os.environ, "PYINSTALLER_RESET_ENVIRONMENT": "1"}


def psq(s):
    return "'" + s.replace("'", "''") + "'"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        try:
            self.logo = tk.PhotoImage(file=str(RES / "assets" / "logo-64.png"))
            self.iconphoto(True, self.logo)
        except tk.TclError:
            self.logo = None
        self.geometry("1320x700")
        self.data = {"items": []}
        self.usr = read_json(USR, {})
        for k, v in (("favoritos", []), ("usos", {}), ("descricoes", {}), ("historico", []), ("manuais", []), ("ocultos", []),
                     ("ultimo", {}), ("notas", {}), ("tags", {}), ("colunas", None)):
            self.usr.setdefault(k, v)
        self.cur_cat, self.rev, self.sortrev, self.icons, self.proc, self.mtime = "__all__", {}, {}, {}, None, 0
        self.usage, self.startup, self.dupg, self.upd, self.upd_info = {}, [], {}, {}, {}
        self.upd_thread = self.upd_result = None
        self.last_focus = 0.0
        self.limpeza_dias = int(config.load().get("limpeza_dias", 180))
        c = read_json(UPD, {})
        self.upd, self.upd_info = c.get("casados", {}), {"quando": c.get("quando"), "total": len(c.get("pacotes", []))}
        self.help_win = self.help_txt = None
        self.menus = []
        self.blank = tk.PhotoImage(width=16, height=16)
        self.dark = system_dark()
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        top = ttk.Frame(self); top.pack(fill="x", padx=8, pady=(6, 2))
        ttk.Label(top, text=tr("Buscar (Ctrl+F):")).pack(side="left")
        self.q = tk.StringVar(); self.q.trace_add("write", lambda *_: self.refresh())
        self.entry = ttk.Entry(top, textvariable=self.q, width=40); self.entry.pack(side="left", padx=6)
        self.entry.bind("<Escape>", lambda e: (self.q.set(""), self.tab.focus_set()))
        self.entry.bind("<Down>", lambda e: self.focus_table())
        self.entry.bind("<Return>", lambda e: self.focus_table())
        self.build_menus(top)
        self.status = ttk.Label(top, text=""); self.status.pack(side="right", padx=10)

        flt = ttk.Frame(self); flt.pack(fill="x", padx=8, pady=(0, 4))
        ttk.Label(flt, text=tr("Disco:")).pack(side="left")
        self.disk = tk.StringVar(value=ALL_DISKS)
        self.cb_disk = ttk.Combobox(flt, textvariable=self.disk, values=[ALL_DISKS], state="readonly", width=14)
        self.cb_disk.pack(side="left", padx=(4, 14))
        ttk.Label(flt, text=tr("Tamanho:")).pack(side="left")
        self.size_f = tk.StringVar(value=ANY_SIZE)
        cb = ttk.Combobox(flt, textvariable=self.size_f, values=list(SIZES), state="readonly", width=18)
        cb.pack(side="left", padx=4)
        for c in (self.cb_disk, cb):
            c.bind("<<ComboboxSelected>>", lambda e: (self.refresh(), self.focus_set()))
        ttk.Button(flt, text=tr("Limpar filtros"), command=self.clear_filters).pack(side="left", padx=14)

        pan = ttk.PanedWindow(self, orient="horizontal"); pan.pack(fill="both", expand=True, padx=8)
        self.after(300, lambda: (self.update_idletasks(), pan.sashpos(0, 300)))
        self.cats = ttk.Treeview(pan, show="tree", selectmode="browse"); pan.add(self.cats, weight=1)
        self.cats.column("#0", width=270)
        self.cats.bind("<<TreeviewSelect>>", self.on_cat)
        right = ttk.Frame(pan); pan.add(right, weight=5)
        cols = tuple(COLS)
        bt = ttk.Frame(right); bt.pack(side="bottom", fill="x", pady=(4, 0))
        self.det = tk.Text(right, height=11, wrap="word", state="disabled", relief="flat", padx=8, pady=6)
        self.det.pack(side="bottom", fill="x", pady=6)
        xb = ttk.Scrollbar(right, orient="horizontal"); xb.pack(side="bottom", fill="x")
        self.tab = ttk.Treeview(right, columns=cols, show="tree headings", selectmode="browse")
        self.tab.heading("#0", text=tr("Nome"), command=lambda: self.sort("#0"))
        self.tab.column("#0", width=270, minwidth=150)
        for c, (title, w) in COLS.items():
            self.tab.heading(c, text=title, command=lambda c=c: self.sort(c))
            self.tab.column(c, width=w, minwidth=40, anchor="e" if c in ("tamanho", "vezes") else "w")
        self.set_columns(self.usr["colunas"] or DEFAULT_COLS)
        sb = ttk.Scrollbar(right, command=self.tab.yview); self.tab.configure(yscrollcommand=sb.set)
        xb.config(command=self.tab.xview); self.tab.configure(xscrollcommand=xb.set)
        sb.pack(side="right", fill="y"); self.tab.pack(side="left", fill="both", expand=True)
        ttk.Button(bt, text=tr("Abrir"), command=self.open_prog).pack(side="left")
        ttk.Button(bt, text=tr("Abrir pasta"), command=self.open_dir).pack(side="left", padx=6)
        ttk.Button(bt, text=tr("★ Favorito"), command=self.toggle_fav).pack(side="left")
        ttk.Button(bt, text=tr("Desinstalar…"), command=self.uninstall).pack(side="left", padx=6)
        ttk.Button(bt, text=tr("Adicionar…"), command=self.add_manual).pack(side="left")
        ttk.Button(bt, text=tr("Notas e tags…"), command=self.edit_notes).pack(side="left", padx=6)
        ttk.Button(bt, text=tr("Atualizar…"), command=self.update_prog).pack(side="left")
        ttk.Button(bt, text=tr("Histórico…"), command=self.show_history).pack(side="right")
        ttk.Button(bt, text=tr("Desfazer (Ctrl+Z)"), command=self.undo).pack(side="right", padx=6)
        self.tab.bind("<<TreeviewSelect>>", lambda e: self.detail())
        self.tab.bind("<Double-1>", lambda e: self.open_prog())
        self.tab.bind("<Return>", lambda e: self.open_prog())
        self.tab.bind("<Button-3>", self.menu)
        self.bind_all("<Control-f>", lambda e: (self.entry.focus_set(), self.entry.select_range(0, "end")))
        self.bind_all("<Control-z>", lambda e: self.undo())
        self.bind_all("<F1>", lambda e: self.show_help())
        self.bind_all("<F5>", lambda e: self.rescan())
        self.bind_all("<Control-e>", lambda e: self.export())
        self.bind_all("<Control-q>", lambda e: self.destroy())
        self.bind("<FocusIn>", self.on_focus)

        self.apply_theme()
        self.load(force=True)
        if not self.data.get("items"):
            self.rescan()

    # ---------- language ----------
    def build_menus(self, top):
        """Top menus (File, View, Tools, Language, Help). Packed from right to left."""
        def make(title, items, side_pad=(0, 4)):
            m = tk.Menu(self, tearoff=0)
            for it in items:
                if it is None:
                    m.add_separator()
                else:
                    label, cmd, acc = it
                    m.add_command(label=label, command=cmd, accelerator=acc)
            self.menus.append(m)
            ttk.Menubutton(top, text=title, menu=m).pack(side="right", padx=side_pad)
            return m

        make(tr("Ajuda"), [(tr("Ajuda"), self.show_help, "F1"), (tr("Abrir página do projeto"), lambda: webbrowser.open(REPO_URL), ""),
                           None, (tr("Sobre o {app}…", app=APP_NAME), self.show_about, "")], (0, 0))
        lang = tk.Menu(self, tearoff=0)
        for code, name in LANGS.items():
            lang.add_command(label=("✓ " if code == LANG else "    ") + name, command=lambda c=code: self.set_lang(c))
        self.menus.append(lang)
        ttk.Menubutton(top, text="🌐 " + tr("Idioma"), menu=lang).pack(side="right", padx=4)
        make(tr("Ferramentas"), [(tr("Verificar atualizações"), self.check_updates, ""),
                                 (tr("Resumo dos programas…"), self.show_summary, ""), None,
                                 (tr("Adicionar programa…"), self.add_manual, ""),
                                 (tr("Desfazer"), self.undo, "Ctrl+Z"), (tr("Histórico de ações…"), self.show_history, "")])
        view = make(tr("Exibir"), [(tr("Alternar tema claro/escuro"), self.toggle_theme, ""),
                                   (tr("Limpar filtros"), self.clear_filters, "")])
        cols = tk.Menu(view, tearoff=0, postcommand=lambda: self.fill_columns_menu(cols))
        self.menus.append(cols)
        view.insert_cascade(1, label=tr("Colunas"), menu=cols)
        make(tr("Arquivo"), [(tr("Reescanear"), self.rescan, "F5"), (tr("Exportar…"), self.export, "Ctrl+E"), None,
                             (tr("Salvar backup da configuração…"), self.backup_save, ""),
                             (tr("Restaurar backup…"), self.backup_restore, ""), None,
                             (tr("Sair"), self.destroy, "Ctrl+Q")])

    def center(self, w):
        """Place the child window over the main window."""
        if not w.winfo_exists():
            return
        w.update_idletasks()
        ww, wh = w.winfo_width(), w.winfo_height()
        if ww < 60:
            ww, wh = w.winfo_reqwidth(), w.winfo_reqheight()
        x = self.winfo_rootx() + max(0, (self.winfo_width() - ww) // 2)
        y = self.winfo_rooty() + max(0, (self.winfo_height() - wh) // 3)
        w.geometry(f"+{x}+{y}")

    def show_about(self):
        w = tk.Toplevel(self); self.after_idle(self.center, w); w.title(tr("Sobre o {app}", app=APP_NAME)); w.transient(self); w.resizable(False, False)
        w.configure(bg=(DARK if self.dark else LIGHT)["bg"]); w.bind("<Escape>", lambda e: w.destroy())
        try:
            w.big = tk.PhotoImage(file=str(RES / "assets" / "logo-256.png")).subsample(2)
            ttk.Label(w, image=w.big).pack(pady=(18, 4))
        except tk.TclError:
            pass
        ttk.Label(w, text=APP_NAME, font=("Segoe UI", 18, "bold")).pack()
        ttk.Label(w, text=tr("Versão {v}", v=VERSION)).pack(pady=(0, 8))
        ttk.Label(w, text=tr("Catálogo dos programas instalados no Windows: o que cada um faz, quando foi usado e quanto ocupa."),
                  wraplength=360, justify="center").pack(padx=24)
        ttk.Label(w, text=tr("Licença MIT • software livre")).pack(pady=(8, 2))
        bar = ttk.Frame(w); bar.pack(pady=14)
        ttk.Button(bar, text=tr("Abrir página do projeto"), command=lambda: webbrowser.open(REPO_URL)).pack(side="left", padx=4)
        ttk.Button(bar, text=tr("Fechar"), command=w.destroy).pack(side="left", padx=4)
        w.grab_set()


    def set_lang(self, code):
        """Save the language and relaunch the app (texts are loaded at startup)."""
        if code == LANG:
            return
        self.usr["idioma"] = code
        self.save_usr()
        if getattr(sys, "frozen", False):
            cmd = [sys.executable]
        else:
            pw = Path(sys.executable).with_name("pythonw.exe")
            cmd = [str(pw if pw.exists() else sys.executable), str(Path(__file__).resolve())]
        subprocess.Popen(cmd, cwd=str(BASE), stdin=subprocess.DEVNULL, creationflags=NOWIN, env=self_env())
        self.destroy()

    # ---------- theme ----------
    def apply_theme(self):
        p, s = (DARK if self.dark else LIGHT), self.style
        self.configure(bg=p["bg"])
        s.configure(".", background=p["bg"], foreground=p["fg"], fieldbackground=p["field"], bordercolor=p["head"],
                    lightcolor=p["head"], darkcolor=p["head"], troughcolor=p["bg"], focuscolor=p["bg"])
        s.configure("Treeview", background=p["field"], fieldbackground=p["field"], foreground=p["fg"], rowheight=22, borderwidth=0)
        s.map("Treeview", background=[("selected", p["sel"])], foreground=[("selected", p["selfg"])])
        s.configure("Treeview.Heading", background=p["head"], foreground=p["fg"], relief="flat")
        s.map("Treeview.Heading", background=[("active", p["sel"])])
        s.configure("TButton", background=p["head"], foreground=p["fg"], padding=(10, 3))
        s.map("TButton", background=[("active", p["sel"])])
        s.configure("TMenubutton", background=p["head"], foreground=p["fg"], padding=(10, 3), arrowcolor=p["fg"])
        s.map("TMenubutton", background=[("active", p["sel"])])
        for db, opt, val in (("background", "background", p["field"]), ("foreground", "foreground", p["fg"]),
                             ("activeBackground", "activebackground", p["sel"]), ("activeForeground", "activeforeground", p["selfg"])):
            self.option_add("*Menu." + db, val)
            for m in self.menus:
                m.configure(**{opt: val})
        s.configure("TEntry", fieldbackground=p["field"], foreground=p["fg"], insertcolor=p["fg"])
        s.configure("TCombobox", fieldbackground=p["field"], background=p["head"], foreground=p["fg"], arrowcolor=p["fg"])
        s.map("TCombobox", fieldbackground=[("readonly", p["field"])], foreground=[("readonly", p["fg"])])
        self.option_add("*TCombobox*Listbox.background", p["field"])
        self.option_add("*TCombobox*Listbox.foreground", p["fg"])
        self.option_add("*TCombobox*Listbox.selectBackground", p["sel"])
        s.configure("TScrollbar", background=p["head"], arrowcolor=p["fg"])
        self.det.config(bg=p["field"], fg=p["fg"], insertbackground=p["fg"])
        self.style_help()

    def toggle_theme(self):
        self.dark = not self.dark
        self.apply_theme()

    # ---------- data ----------
    @property
    def scan_items(self):
        return self.data.setdefault("items", [])

    @property
    def items(self):
        """Scan items plus those added manually (without repeating the same executable)."""
        have = {x.get("target") for x in self.scan_items}
        return self.scan_items + [m for m in self.usr["manuais"] if m.get("target") not in have]

    def save_idx(self):
        write_json(IDX, self.data)
        self.mtime = IDX.stat().st_mtime

    def save_usr(self):
        write_json(USR, self.usr)

    def load(self, force=False):
        try:
            m = IDX.stat().st_mtime
        except OSError:
            return
        if m == self.mtime and not force:
            return
        d = read_json(IDX, {})
        self.data = d if isinstance(d, dict) else {"items": d}
        self.mtime = m
        disks = sorted({disk_of(i) for i in self.items})
        self.cb_disk.config(values=[ALL_DISKS] + disks)
        if self.disk.get() not in [ALL_DISKS] + disks:
            self.disk.set(ALL_DISKS)
        self.refresh_usage(redraw=False)
        self.refresh()

    # ---------- usage, startup, duplicates ----------
    def refresh_usage(self, redraw=True):
        """Re-read usage (Windows UserAssist + launches from this program), startup entries and duplicates."""
        try:
            ua = usage.userassist(); by = usage.usage_index(ua); self.startup = usage.startup_entries()
        except Exception:
            ua, by, self.startup = {}, {}, []
        items = self.items
        self.usage = {}
        for i in items:
            n, t = usage.usage_of(i, ua, by)
            on = self.usr["usos"].get(i["name"], 0)
            try: ot = datetime.datetime.fromisoformat(self.usr["ultimo"].get(i["name"], ""))
            except ValueError: ot = None
            self.usage[i["name"]] = (max(n, on), max([x for x in (t, ot) if x], default=None))
        self.dupg = {}
        for base, grp in usage.dup_groups([i for i in items if i["name"] not in set(self.usr["ocultos"])]).items():
            tot = self.uniq_size(grp)
            for i in grp:
                self.dupg[i["name"]] = (base, len(grp), tot)
        if redraw:
            self.refresh()

    def on_focus(self, e):
        if e.widget is self and time.time() - self.last_focus > 20:     # when returning to the window, refresh usage
            self.last_focus = time.time()
            self.refresh_usage()

    def uniq_size(self, items):
        """Sum of sizes without counting the same folder twice (several shortcuts of the same program)."""
        seen, tot = set(), 0
        for i in items:
            k = (i.get("location") or i["name"]).lower()
            if k not in seen and i.get("size"):
                seen.add(k); tot += i["size"]
        return tot

    def startup_state(self, i):
        e = usage.startup_of(i, self.startup)
        return None if not e else ("Sim" if e["ativo"] else "Desativado")

    def purpose(self, i):
        return self.usr["descricoes"].get(i["name"]) or i.get("purpose") or ""

    def sub(self, i):
        return i.get("sub") or "Geral"

    def last_used(self, i):
        return self.usage.get(i["name"], (0, None))

    def old_candidates(self, data):
        lim = datetime.datetime.now() - datetime.timedelta(days=self.limpeza_dias)
        fav = set(self.usr["favoritos"])
        out = [i for i in data if not i.get("broken") and i["category"] not in ("Sistema", "Atalhos quebrados")
               and i["name"] not in fav and (self.last_used(i)[1] is None or self.last_used(i)[1] < lim)]
        return sorted(out, key=lambda i: -(i.get("size") or 0))

    def set_columns(self, cols):
        cols = [c for c in cols if c in COLS] or DEFAULT_COLS
        self.usr["colunas"] = cols
        self.tab.configure(displaycolumns=cols)

    def fill_columns_menu(self, m):
        m.delete(0, "end")
        for c, (title, _) in COLS.items():
            v = tk.BooleanVar(value=c in self.usr["colunas"])
            def tog(c=c):
                cur = [x for x in COLS if (x in self.usr["colunas"]) != (x == c)]
                self.set_columns(cur); self.save_usr()
            m.add_checkbutton(label=title, variable=v, command=tog)
        m.add_separator()
        m.add_command(label=tr("Restaurar colunas padrão"), command=lambda: (self.set_columns(DEFAULT_COLS), self.save_usr()))

    def col_menu(self, e):
        m = tk.Menu(self, tearoff=0)
        self.fill_columns_menu(m)
        m.tk_popup(e.x_root, e.y_root)

    def filters_active(self):
        return bool(self.q.get() or self.disk.get() != ALL_DISKS or self.size_f.get() != ANY_SIZE)

    def clear_filters(self):
        self.q.set(""); self.disk.set(ALL_DISKS); self.size_f.set(ANY_SIZE)
        self.refresh()

    def filtered(self):
        hid = set(self.usr["ocultos"])
        return [i for i in self.filtered_all() if i["name"] not in hid]

    def hidden_list(self):
        hid = set(self.usr["ocultos"])
        return [i for i in self.filtered_all() if i["name"] in hid]

    def pool(self):
        return self.hidden_list() if self.cur_cat == "__hid__" else self.filtered()

    def filtered_all(self):
        q, disk, fn = self.q.get().lower(), self.disk.get(), SIZES.get(self.size_f.get())
        out = []
        for i in self.items:
            if q and q not in " ".join([i["name"], self.purpose(i), trd(self.purpose(i)), i.get("location", ""), i["category"],
                                        trc(i["category"]), self.sub(i), trc(self.sub(i)),
                                        i.get("company") or "", self.usr["notas"].get(i["name"], ""),
                                        " ".join(self.usr["tags"].get(i["name"], []))]).lower():
                continue
            if disk != ALL_DISKS and disk_of(i) != disk:
                continue
            if fn and not fn(i.get("size")):
                continue
            out.append(i)
        return out

    def members(self, cat, data):
        fav = set(self.usr["favoritos"])
        if cat == "__all__": return data
        if cat == "__fav__": return [i for i in data if i["name"] in fav]
        if cat == "__top__":
            return sorted([i for i in data if self.last_used(i)[0] > 0], key=lambda i: -self.last_used(i)[0])[:15]
        if cat == "__old__": return self.old_candidates(data)
        if cat == "__start__": return [i for i in data if self.startup_state(i) == "Sim"]
        if cat == "__upd__": return [i for i in data if i["name"] in self.upd]
        if cat == "__dup__":
            return sorted([i for i in data if i["name"] in self.dupg], key=lambda i: (self.dupg[i["name"]][0], i["name"].lower()))
        if cat == "__tags__": return [i for i in data if self.usr["tags"].get(i["name"])]
        if cat.startswith("tag::"): return [i for i in data if cat[5:] in self.usr["tags"].get(i["name"], [])]
        if cat == "__new__": return [i for i in data if i.get("novo")]
        if cat == "__nolnk__": return [i for i in data if i.get("sematalho")]
        if cat == "__hid__": return data
        if "||" in cat:
            c, s = cat.split("||", 1)
            return [i for i in data if i["category"] == c and self.sub(i) == s]
        return [i for i in data if i["category"] == cat]

    def refresh(self):
        data = self.filtered()
        opened = {c for c in self.cats.get_children() if self.cats.item(c, "open")}
        spread = self.filters_active()
        self.cats.delete(*self.cats.get_children())
        for iid, label in VIRTUAL:
            n = len(self.members(iid, data))
            if iid == "__all__" or n:
                self.cats.insert("", "end", iid=iid, text=f"{label} ({n})")
        nh = len(self.hidden_list())
        if nh:
            self.cats.insert("", "end", iid="__hid__", text=f"{tr('Ocultos')} ({nh})")
        tagset = sorted({t for i in data for t in self.usr["tags"].get(i["name"], [])})
        if tagset:
            self.cats.insert("", "end", iid="__tags__", text=f"{tr('Tags')} ({len(self.members('__tags__', data))})",
                             open=("__tags__" in opened or self.cur_cat.startswith("tag::")))
            for t in tagset:
                self.cats.insert("__tags__", "end", iid=f"tag::{t}", text=f"#{t} ({len(self.members('tag::' + t, data))})")
        for c in sorted({i["category"] for i in data}, key=lambda c: (c == "Atalhos quebrados", trc(c).lower())):
            self.cats.insert("", "end", iid=c, text=f"{trc(c)} ({len(self.members(c, data))})",
                             open=(c in opened or spread or self.cur_cat.startswith(c + "||")))
            for s in sorted({self.sub(i) for i in data if i["category"] == c}, key=lambda s: trc(s).lower()):
                iid = f"{c}||{s}"
                self.cats.insert(c, "end", iid=iid, text=f"{trc(s)} ({len(self.members(iid, data))})")
        if not self.cats.exists(self.cur_cat):
            self.cur_cat = "__all__"
        self.cats.selection_set(self.cur_cat)
        self.fill_table()
        head, extra = [tr("{n} programas", n=len(data))], []
        if self.data.get("sizing"): head.append(tr("calculando tamanhos…"))
        nv = sum(1 for i in self.items if i.get("novo"))
        if nv: extra.append(tr("{n} novo(s)", n=nv))
        if self.data.get("removidos"): extra.append(tr("{n} removido(s)", n=len(self.data["removidos"])))
        if self.cur_cat == "__old__":
            extra.append(tr("liberaria até {size} (sem uso há {dias}+ dias ou sem registro)", size=fmt(self.uniq_size(self.members("__old__", data))), dias=self.limpeza_dias))
        if self.upd_info.get("quando") and self.upd:
            extra.append(tr("{n} com atualização", n=len(self.upd)))
        self.status_parts = (head, extra)
        self.show_status()

    def show_status(self):
        """Status bar text; the "scanned … ago" part is recomputed every minute."""
        head, extra = self.status_parts
        age = self.scan_age()
        mid = [tr("escaneado {quando}", quando=age)] if age else []
        self.status.config(text=" • ".join(head + mid + extra))
        if getattr(self, "status_job", None): self.after_cancel(self.status_job)
        self.status_job = self.after(60000, self.show_status)

    def scan_age(self):
        """How long ago index.json was generated ("5 min ago", "yesterday"…), or "" if unknown."""
        try:
            dt = datetime.datetime.strptime(self.data.get("gerado", ""), "%Y-%m-%d %H:%M")
        except ValueError:
            return ""
        mins = int((datetime.datetime.now() - dt).total_seconds() // 60)
        if mins < 1: return tr("agora há pouco")
        if mins < 60: return tr("há {n} min", n=mins)
        if mins < 24 * 60 and dt.date() == datetime.date.today(): return tr("há {n} h", n=mins // 60)
        return usage.rel_days(dt)

    def on_cat(self, e):
        s = self.cats.selection()
        if s and s[0] != self.cur_cat:
            self.cur_cat = s[0]
            self.fill_table()

    def icon(self, i):
        t = i.get("target") or ""
        if not t:
            return self.blank
        k = hashlib.sha1(t.lower().encode("utf-8")).hexdigest()[:16]
        if k not in self.icons:
            try:
                self.icons[k] = tk.PhotoImage(file=str(ICONS / f"{k}.png"))
            except tk.TclError:
                self.icons[k] = self.blank
        return self.icons[k]

    def fill_table(self):
        prev = self.cur() and self.cur()["name"]
        self.tab.delete(*self.tab.get_children())
        self.rev = {}
        fav = set(self.usr["favoritos"])
        for n, i in enumerate(self.members(self.cur_cat, self.pool())):
            iid = str(n); self.rev[iid] = i
            name = ("★ " if i["name"] in fav else "") + i["name"] + ("  " + tr("(novo)") if i.get("novo") else "")
            n, t = self.last_used(i)
            ultimo = f"{t.strftime(tr('%d/%m/%Y'))} · {usage.rel_days(t)}" if t else (tr("sem registro") if i.get("target") else "")
            u = self.upd.get(i["name"])
            self.tab.insert("", "end", iid=iid, text=name, image=self.icon(i),
                            values=(i.get("ver") or "", f"→ {u['nova']}" if u else "", fmt(i.get("size")), disk_of(i),
                                    ultimo, n or "", fmt_date(i.get("instalado")), tr(self.startup_state(i) or ""),
                                    ", ".join(self.usr["tags"].get(i["name"], [])),
                                    f"{trc(i['category'])} › {trc(self.sub(i))}", i.get("location", "")))
            if i["name"] == prev:
                self.tab.selection_set(iid)

    def sort(self, col):
        rev = self.sortrev[col] = not self.sortrev.get(col, True)
        def key(k):
            i = self.rev[k]
            t = self.last_used(i)[1]
            return {"#0": i["name"].lower(), "versao": (i.get("ver") or "").lower(), "tamanho": i.get("size") or -1,
                    "disco": disk_of(i), "cat": (trc(i["category"]) + trc(self.sub(i))).lower(),
                    "local": i.get("location", "").lower(), "upd": i["name"] in self.upd,
                    "ultimo": t.timestamp() if t else -1, "vezes": self.last_used(i)[0],
                    "instalado": i.get("instalado") or "", "inicia": self.startup_state(i) or "",
                    "tags": ", ".join(self.usr["tags"].get(i["name"], [])).lower()}[col]
        for p, k in enumerate(sorted(self.tab.get_children(), key=key, reverse=rev)):
            self.tab.move(k, "", p)

    def cur(self):
        s = self.tab.selection()
        return self.rev.get(s[0]) if s else None

    def focus_table(self):
        self.tab.focus_set()
        k = self.tab.get_children()
        if k and not self.tab.selection():
            self.tab.selection_set(k[0]); self.tab.focus(k[0])
        return "break"

    def detail(self):
        i = self.cur()
        if not i: return
        flags = [tr(f) for f, on in (("novo", i.get("novo")), ("sem atalho no Menu Iniciar", i.get("sematalho")),
                                     ("atalho quebrado", i.get("broken"))) if on]
        if i.get("launcher") or i.get("manual"):
            un = tr("não se aplica (programa aberto por arquivo/pasta; para remover, apague a pasta com 'Abrir pasta')")
        elif i.get("uninstall"):
            un = tr("disponível (registro do Windows: {nome})", nome=i.get("uninstall_nome") or "—")
        else:
            un = tr("não encontrado (programa portátil ou sem desinstalador registrado)")
        n, lt = self.last_used(i)
        u, dg, st = self.upd.get(i["name"]), self.dupg.get(i["name"]), self.startup_state(i)
        tags, nota = self.usr["tags"].get(i["name"], []), self.usr["notas"].get(i["name"], "")
        lt_txt = lt.strftime(tr("%d/%m/%Y") + " %H:%M") + f" ({usage.rel_days(lt)})" if lt else tr("sem registro")
        ver_upd = "  (" + tr("winget: {v} disponível", v=u["nova"]) + ")" if u else ""
        abertos = tr("aberto {n}x por aqui", n=self.usr["usos"].get(i["name"], 0))
        dup = tr("Versões duplicadas: grupo «{g}» com {n} itens ({size} no total)", g=dg[0], n=dg[1], size=fmt(dg[2])) + "\n" if dg else ""
        nv = len(i.get("variants", [])) - 1
        via = ""
        if (i.get("launcher") or i.get("manual")) and i.get("target"):
            via = (f"{tr('Abre por')}: {os.path.basename(i['target'])}"
                   + (" " + tr("(+{n} variante(s): botão direito > Abrir variante)", n=nv) if nv > 0 else "") + "\n")
        t = (f"{i['name']}" + (f"   [{', '.join(flags)}]" if flags else "") +
             f"\n{tr('Categoria')}: {trc(i['category'])} › {trc(self.sub(i))}   {tr('Disco')}: {disk_of(i)}\n"
             f"{tr('Versão')}: {i.get('ver') or '—'}{ver_upd}   {tr('Fabricante')}: {i.get('company') or '—'}\n"
             f"{tr('Último uso')}: {lt_txt}   {tr('Vezes usado')}: {n or '—'}   "
             f"({abertos})   {tr('Instalado em')}: {fmt_date(i.get('instalado')) or '—'}\n"
             f"{tr('Tamanho')}: {fmt(i.get('size'))}\n{tr('Local')}: {i.get('location') or '—'}\n"
             + (f"{tr('Inicia com o Windows')}: {tr(st)}\n" if st else "") + dup
             + (f"{tr('Tags')}: {', '.join(tags)}\n" if tags else "") + (f"{tr('Notas')}: {nota}\n" if nota else "") + via
             + f"{tr('Desinstalar')}: {un}\n"
             + f"{tr('Para que serve')}: {trd(self.purpose(i)) or tr('sem descrição (botão direito > Editar descrição…)')}")
        self.det.config(state="normal"); self.det.delete("1.0", "end"); self.det.insert("1.0", t)
        self.det.config(state="disabled")

    # ---------- history / undo ----------
    def log(self, tipo, nome, txt, undo=None):
        self.usr["historico"].append({"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "tipo": tipo, "nome": nome,
                                      "txt": txt, "undo": undo, "revertido": False})
        del self.usr["historico"][:-HIST_MAX]
        self.save_usr()

    def undo(self, entry=None):
        hist = self.usr["historico"]
        e = entry or next((h for h in reversed(hist) if h.get("undo") and not h.get("revertido")), None)
        if not e:
            messagebox.showinfo(tr("Desfazer"), tr("Não há nada para desfazer."), parent=self)
            return
        if e.get("revertido") or not e.get("undo"):
            messagebox.showinfo(tr("Desfazer"), tr("Esta ação não pode ser revertida pelo app."), parent=self)
            return
        u, n = e["undo"], e["nome"]
        try:
            if e["tipo"] == "favorito":
                f = self.usr["favoritos"]
                if u["antes"] and n not in f: f.append(n)
                if not u["antes"] and n in f: f.remove(n)
            elif e["tipo"] == "descricao":
                if u["antes"] is None: self.usr["descricoes"].pop(n, None)
                else: self.usr["descricoes"][n] = u["antes"]
            elif e["tipo"] == "categoria":
                cfg = config.load_local(); ov = cfg.setdefault("overrides", {})
                if u["over"] is None: ov.pop(n, None)
                else: ov[n] = u["over"]
                config.save_local(cfg)
                for i in self.items:
                    if i["name"] == n:
                        i["category"], i["sub"] = u["cat"], u["sub"]
                self.save_idx()
            elif e["tipo"] == "notas":
                for k, key in (("nota", "notas"), ("tags", "tags")):
                    if u[k] is None: self.usr[key].pop(n, None)
                    else: self.usr[key][n] = u[k]
            elif e["tipo"] == "restaurar":
                self.apply_snapshot(u["antes"])
            elif e["tipo"] == "ocultar":
                o = self.usr["ocultos"]
                if u["antes"] and n not in o: o.append(n)
                if not u["antes"] and n in o: o.remove(n)
            elif e["tipo"] == "adicionar":
                self.usr["manuais"] = [m for m in self.usr["manuais"] if m["name"] != n]
            elif e["tipo"] == "remover":
                if not any(m["name"] == n for m in self.usr["manuais"]):
                    self.usr["manuais"].append(u["item"])
            elif e["tipo"] == "lixeira":
                self.restore_lnk(u["backup"], u["orig"], lambda: self.finish_restore(e))
                return
        except OSError as ex:
            messagebox.showerror(tr("Desfazer"), str(ex), parent=self)
            return
        e["revertido"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_usr(); self.refresh_usage(redraw=False); self.refresh(); self.detail()
        self.status.config(text=tr("Desfeito: {txt}", txt=e["txt"]))

    def restore_lnk(self, backup, orig, done):
        """Copy the shortcut back. If permission is missing, retry as administrator (asks for password/confirmation)."""
        if not os.path.exists(backup):
            messagebox.showerror(tr("Desfazer"), tr("A cópia de segurança não existe mais:\n{p}", p=backup), parent=self)
            return False
        try:
            Path(orig).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, orig)
            done()
            return True
        except OSError:
            if not messagebox.askyesno(tr("Desfazer"), tr("Sem permissão para recriar o atalho nesta pasta.\n"
                                       "Tentar como administrador (o Windows pedirá confirmação/senha)?"), parent=self):
                return False
            self.run_admin(f"Copy-Item -LiteralPath {psq(backup)} -Destination {psq(orig)} -Force",
                           lambda rc: done() if os.path.exists(orig) else
                           messagebox.showerror(tr("Desfazer"), tr("Não foi possível restaurar o atalho."), parent=self))
            return True

    def finish_restore(self, e):
        if not os.path.exists(e["undo"]["orig"]):
            return
        item = e["undo"]["item"]
        if not any(i["name"] == item["name"] and i.get("lnk") == item.get("lnk") for i in self.items):
            self.data["items"].append(item)
            self.data["items"].sort(key=lambda i: (i["category"], i.get("sub", ""), i["name"].lower()))
            self.save_idx()
        e["revertido"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.save_usr(); self.refresh()
        self.status.config(text=tr("Desfeito: {txt}", txt=e["txt"]))

    def show_history(self):
        w = tk.Toplevel(self); self.after_idle(self.center, w); w.title(tr("Histórico de ações")); w.geometry("820x420"); w.transient(self)
        w.configure(bg=(DARK if self.dark else LIGHT)["bg"])
        cols = ("quando", "acao", "estado")
        t = ttk.Treeview(w, columns=cols, show="headings", selectmode="browse")
        for c, h, wd in (("quando", tr("Quando"), 140), ("acao", tr("Ação"), 520), ("estado", tr("Estado"), 130)):
            t.heading(c, text=h); t.column(c, width=wd)
        t.pack(fill="both", expand=True, padx=8, pady=8)
        rows = {}

        def fill():
            t.delete(*t.get_children()); rows.clear()
            for n, h in enumerate(reversed(self.usr["historico"])):
                st = tr("revertido") if h.get("revertido") else (tr("pode reverter") if h.get("undo") else tr("irreversível pelo app"))
                iid = str(n); rows[iid] = h
                t.insert("", "end", iid=iid, values=(h["quando"], h["txt"], st))
        fill()

        def rev():
            s = t.selection()
            if s:
                self.undo(rows[s[0]]); fill()
        bar = ttk.Frame(w); bar.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Button(bar, text=tr("Reverter selecionado"), command=rev).pack(side="left")
        ttk.Button(bar, text=tr("Fechar"), command=w.destroy).pack(side="right")
        w.bind("<Escape>", lambda e: w.destroy())

    # ---------- administrator (asks for the Windows password/confirmation) ----------
    def run_admin(self, script, done):
        f = tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8-sig")
        f.write(script); f.close()
        outer = ("Start-Process powershell -Verb RunAs -Wait -WindowStyle Hidden -ArgumentList "
                 f"'-NoProfile','-ExecutionPolicy','Bypass','-File',{psq(f.name)}")
        p = subprocess.Popen(["powershell", "-NoProfile", "-Command", outer], creationflags=NOWIN, stdin=subprocess.DEVNULL)

        def chk():
            if p.poll() is None:
                self.after(500, chk)
            else:
                try: os.unlink(f.name)
                except OSError: pass
                done(p.returncode)
        chk()

    # ---------- actions ----------
    def open_prog(self, target=None):
        i = self.cur()
        if not i: return
        tgt = target or (i.get("lnk") if i.get("lnk") and os.path.exists(i["lnk"]) else i.get("target"))
        if not tgt or not os.path.exists(tgt):
            messagebox.showinfo(tr("Abrir"), tr("Não há executável conhecido para este item.")
                                + (tr("\nUse 'Abrir pasta'.") if i.get("location") else ""))
            return
        try:
            wd = os.path.dirname(tgt) if not tgt.lower().endswith(".lnk") else None
            if tgt.lower().endswith(".ps1"):     # a .ps1 would open in the editor: run it in PowerShell
                subprocess.Popen(["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", tgt], cwd=wd)
            elif wd:
                os.startfile(tgt, cwd=wd)         # .bat/.cmd scripts must run in their own folder
            else:
                os.startfile(tgt)
            self.usr["usos"][i["name"]] = self.usr["usos"].get(i["name"], 0) + 1
            self.usr["ultimo"][i["name"]] = datetime.datetime.now().isoformat(timespec="seconds")
            self.save_usr()
            self.refresh_usage(redraw=False)
            self.fill_table()
            self.detail()
        except OSError as e:
            messagebox.showerror(tr("Erro"), str(e))

    def open_dir(self):
        i = self.cur()
        if i and i.get("location") and os.path.isdir(i["location"]):
            os.startfile(i["location"])

    def toggle_fav(self):
        i = self.cur()
        if not i: return
        f, was = self.usr["favoritos"], i["name"] in self.usr["favoritos"]
        f.remove(i["name"]) if was else f.append(i["name"])
        self.log("favorito", i["name"], tr("Removeu dos favoritos: {n}" if was else "Adicionou aos favoritos: {n}", n=i["name"]), {"antes": was})
        self.refresh()

    def edit_desc(self):
        i = self.cur()
        if not i: return
        r = simpledialog.askstring(tr("Para que serve"), tr("Descrição de {n}:", n=i["name"]),
                                   initialvalue=trd(self.purpose(i)), parent=self)
        if r is None: return
        antes = self.usr["descricoes"].get(i["name"])
        if r.strip(): self.usr["descricoes"][i["name"]] = r.strip()
        else: self.usr["descricoes"].pop(i["name"], None)
        self.log("descricao", i["name"], tr("Editou a descrição de {n}", n=i["name"]), {"antes": antes})
        self.detail()

    # ---------- notes and tags ----------
    def edit_notes(self):
        i = self.cur()
        if not i:
            messagebox.showinfo(tr("Notas e tags"), tr("Selecione um programa na lista."), parent=self); return
        n = i["name"]
        w = tk.Toplevel(self); self.after_idle(self.center, w); w.title(tr("Notas e tags — {n}", n=n)); w.geometry("520x330"); w.transient(self); w.grab_set()
        p = DARK if self.dark else LIGHT
        w.configure(bg=p["bg"])
        ttk.Label(w, text=tr("Tags (separadas por vírgula, ex.: trabalho, estudo):")).pack(anchor="w", padx=10, pady=(10, 2))
        tv = tk.StringVar(value=", ".join(self.usr["tags"].get(n, [])))
        ttk.Entry(w, textvariable=tv).pack(fill="x", padx=10)
        ttk.Label(w, text=tr("Notas (licença, onde baixou, para que projeto serve…):")).pack(anchor="w", padx=10, pady=(10, 2))
        tx = tk.Text(w, height=9, wrap="word", bg=p["field"], fg=p["fg"], insertbackground=p["fg"], relief="flat", padx=6, pady=4)
        tx.pack(fill="both", expand=True, padx=10); tx.insert("1.0", self.usr["notas"].get(n, ""))

        def save():
            tags = []
            for t in re.split(r"[,;]", tv.get()):
                t = t.strip().lstrip("#")
                if t and t.lower() not in [x.lower() for x in tags]: tags.append(t)
            nota = tx.get("1.0", "end").strip()
            antes = {"nota": self.usr["notas"].get(n), "tags": self.usr["tags"].get(n)}
            if nota: self.usr["notas"][n] = nota
            else: self.usr["notas"].pop(n, None)
            if tags: self.usr["tags"][n] = tags
            else: self.usr["tags"].pop(n, None)
            self.log("notas", n, tr("Editou notas/tags de {n}", n=n), antes)
            w.destroy(); self.refresh(); self.detail()
        bar = ttk.Frame(w); bar.pack(fill="x", padx=10, pady=10)
        ttk.Button(bar, text=tr("Salvar"), command=save).pack(side="right")
        ttk.Button(bar, text=tr("Cancelar"), command=w.destroy).pack(side="right", padx=6)
        w.bind("<Escape>", lambda e: w.destroy())

    # ---------- updates (winget) ----------
    def check_updates(self):
        if self.upd_thread and self.upd_thread.is_alive():
            return
        self.status.config(text=tr("Verificando atualizações (winget, ~15 s)…"))
        self.upd_result = None

        def work():
            try: self.upd_result = ("ok", usage.winget_upgrades())
            except Exception as ex: self.upd_result = ("erro", str(ex))
        self.upd_thread = threading.Thread(target=work, daemon=True); self.upd_thread.start()
        self.after(700, self.poll_upd)

    def poll_upd(self):
        if self.upd_thread and self.upd_thread.is_alive():
            self.after(700, self.poll_upd); return
        kind, val = self.upd_result or ("erro", tr("sem resposta"))
        if kind == "erro":
            messagebox.showerror(tr("Atualizações"), tr("Não consegui consultar o winget:\n{v}", v=val), parent=self)
            self.refresh(); return
        self.upd = usage.match_updates(self.items, val)
        self.upd_info = {"quando": time.strftime("%Y-%m-%d %H:%M"), "total": len(val)}
        write_json(UPD, {"quando": self.upd_info["quando"], "pacotes": val, "casados": self.upd})
        self.refresh()
        messagebox.showinfo(tr("Atualizações"), tr("O winget informou {a} pacote(s) com versão nova.\n"
                            "{b} deles correspondem a itens desta lista (categoria «Com atualização», coluna Atualização).\n"
                            "Os demais são componentes do Windows, drivers ou programas que não estão no índice.", a=len(val), b=len(self.upd)), parent=self)

    def update_prog(self):
        i = self.cur()
        u = i and self.upd.get(i["name"])
        if not u:
            messagebox.showinfo(tr("Atualizar"), tr("Este item não tem atualização conhecida.\nClique em «Verificar atualizações» para consultar o winget."), parent=self)
            return
        if not messagebox.askyesno(tr("Atualizar"), tr("Atualizar «{n}» de {a} para {b} pelo winget?\n\n"
                                   "Pacote: {id}\nUma janela de console mostrará o andamento e o Windows pode pedir confirmação de administrador.\n"
                                   "O app não consegue desfazer uma atualização.", n=i["name"], a=u["atual"], b=u["nova"], id=u["id"]), parent=self):
            return
        cmd = f'winget upgrade --id {u["id"]} -e --accept-source-agreements --accept-package-agreements & pause'
        subprocess.Popen(["cmd", "/c", cmd], creationflags=0x10)       # CREATE_NEW_CONSOLE
        self.log("atualizar", i["name"], tr("Iniciou a atualização de {n} ({a} → {b}) pelo winget", n=i["name"], a=u["atual"], b=u["nova"]), None)

    # ---------- summary ----------
    def show_summary(self):
        w = tk.Toplevel(self); self.after_idle(self.center, w); w.title(tr("Resumo dos programas")); w.geometry("980x720"); w.transient(self)
        p = DARK if self.dark else LIGHT
        w.configure(bg=p["bg"]); w.bind("<Escape>", lambda e: w.destroy())
        cv = tk.Canvas(w, bg=p["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(w, command=cv.yview); cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y"); cv.pack(fill="both", expand=True)
        hid = set(self.usr["ocultos"])
        items = [i for i in self.items if i["name"] not in hid and not i.get("broken")]
        y = [14]
        font_h, font_t = ("Segoe UI", 12, "bold"), ("Segoe UI", 10)

        def title(t):
            y[0] += 8; cv.create_text(16, y[0], anchor="nw", text=t, font=font_h, fill=p["fg"]); y[0] += 28

        def line(t):
            cv.create_text(24, y[0], anchor="nw", text=t, font=font_t, fill=p["fg"]); y[0] += 20

        def bars(rows):
            top = max([v for _, v, _ in rows] + [1]); wmax = 420
            for lab, v, txt in rows:
                cv.create_text(24, y[0], anchor="nw", text=lab[:34], font=font_t, fill=p["fg"])
                cv.create_rectangle(250, y[0] + 2, 250 + max(2, int(wmax * v / top)), y[0] + 16, fill=p["sel"] if not self.dark else "#4f86d6", width=0)
                cv.create_text(250 + max(2, int(wmax * v / top)) + 8, y[0], anchor="nw", text=txt, font=font_t, fill=p["fg"]); y[0] += 22

        old = self.old_candidates(items)
        title(tr("Visão geral"))
        line(tr("{n} programas • espaço em disco: {size} (pastas contadas uma vez)", n=len(items), size=fmt(self.uniq_size(items))))
        line(tr("Sem uso há {dias}+ dias ou sem registro: {n} programas, até {size} (categoria «Sugestão de limpeza»)", dias=self.limpeza_dias, n=len(old), size=fmt(self.uniq_size(old))))
        line(tr("Iniciam com o Windows: {a} • Com atualização: {b}", a=len(self.members("__start__", items)), b=len(self.upd))
             + (tr(" (verificado em {q})", q=self.upd_info["quando"]) if self.upd_info.get("quando") else tr(" (clique em «Verificar atualizações»)")))
        groups = {v[0] for v in self.dupg.values()}
        line(tr("Versões duplicadas: {n} grupo(s)", n=len(groups)) + (tr(", {n} itens ocupando {size}", n=len(self.dupg), size=fmt(sum(self.uniq_size([i for i in items if self.dupg.get(i["name"], ("",))[0] == g]) for g in groups))) if groups else ""))
        title(tr("Espaço por categoria"))
        bars([(trc(c), s, fmt(s)) for c, s in sorted(((c, self.uniq_size([i for i in items if i["category"] == c]))
                                                   for c in {i["category"] for i in items}), key=lambda x: -x[1])[:12]])
        title(tr("Espaço por disco"))
        bars([(d, s, fmt(s)) for d, s in sorted(((d, self.uniq_size([i for i in items if disk_of(i) == d]))
                                                  for d in {disk_of(i) for i in items}), key=lambda x: -x[1])])
        title(tr("Maiores programas"))
        seen, top = set(), []
        for i in sorted(items, key=lambda i: -(i.get("size") or 0)):
            k = (i.get("location") or i["name"]).lower()
            if k not in seen and i.get("size"):
                seen.add(k); top.append(i)
            if len(top) == 10: break
        bars([(i["name"], i["size"], fmt(i["size"])) for i in top])
        title(tr("Mais usados"))
        used = sorted([i for i in items if self.last_used(i)[0] > 0], key=lambda i: -self.last_used(i)[0])[:10]
        bars([(i["name"], self.last_used(i)[0], f"{self.last_used(i)[0]}x") for i in used]) if used else line(tr("Ainda sem registros de uso."))
        title(tr("Instalações por ano"))
        yrs = {}
        for i in items:
            if i.get("instalado"): yrs[i["instalado"][:4]] = yrs.get(i["instalado"][:4], 0) + 1
        bars([(k, v, str(v)) for k, v in sorted(yrs.items())]) if yrs else line(tr("Sem datas de instalação."))
        line(tr("Os números de uso vêm do registro do Windows (UserAssist) e das aberturas feitas por este programa."))
        cv.configure(scrollregion=(0, 0, 900, y[0] + 20))
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(-1 * (e.delta // 120), "units") if cv.winfo_exists() else None)

    # ---------- configuration backup ----------
    def snapshot(self):
        cfg = config.load_local()
        return {"formato": BACKUP_FORMAT, "quando": time.strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": {k: self.usr.get(k) for k in KEEP}, "overrides": cfg.get("overrides", {})}

    def apply_snapshot(self, snap):
        for k in KEEP:
            if k in snap["usuario"] and snap["usuario"][k] is not None:
                self.usr[k] = snap["usuario"][k]
            elif k in ("colunas",):
                self.usr[k] = None
        cfg = config.load_local(); cfg["overrides"] = snap.get("overrides", {}); config.save_local(cfg)
        self.set_columns(self.usr["colunas"] or DEFAULT_COLS)
        self.save_usr()

    def backup_save(self):
        path = filedialog.asksaveasfilename(parent=self, defaultextension=".json", initialfile=f"app-manager-backup-{time.strftime('%Y%m%d')}",
                                            filetypes=[(tr("Backup do {app}", app=APP_NAME), "*.json")])
        if not path: return
        write_json(Path(path), self.snapshot())
        messagebox.showinfo(tr("Backup"), tr("Backup salvo (favoritos, usos, notas, tags, descrições, ocultos, itens adicionados e categorias movidas)."), parent=self)

    def backup_restore(self):
        path = filedialog.askopenfilename(parent=self, filetypes=[(tr("Backup do {app}", app=APP_NAME), "*.json")])
        if not path: return
        snap = read_json(Path(path), None)
        if not isinstance(snap, dict) or snap.get("formato") not in (BACKUP_FORMAT, "indice-backup-1") or not isinstance(snap.get("usuario"), dict):
            messagebox.showerror(tr("Backup"), tr("Este arquivo não parece ser um backup do {app}.", app=APP_NAME), parent=self); return
        r = messagebox.askyesnocancel(tr("Restaurar backup"), tr("Backup de {q}.\n\nSim = mesclar com o que existe hoje\n"
                                      "Não = substituir tudo pelo conteúdo do backup\nCancelar = não fazer nada\n\n"
                                      "Dá para desfazer pelo Histórico.", q=snap.get("quando", "?")), parent=self)
        if r is None: return
        antes = self.snapshot()
        BACKUPS.mkdir(exist_ok=True); write_json(BACKUPS / f"config-antes-{time.strftime('%Y%m%d-%H%M%S')}.json", antes)
        if r:                                              # merge
            new = json.loads(json.dumps(antes))
            for k, v in snap["usuario"].items():
                if isinstance(v, list) and isinstance(new["usuario"].get(k), list):
                    seen = {json.dumps(x, sort_keys=True) for x in new["usuario"][k]}
                    new["usuario"][k] += [x for x in v if json.dumps(x, sort_keys=True) not in seen]
                elif isinstance(v, dict) and isinstance(new["usuario"].get(k), dict):
                    new["usuario"][k].update(v)
                elif v is not None:
                    new["usuario"][k] = v
            new["overrides"] = {**antes["overrides"], **snap.get("overrides", {})}
            snap = new
        self.apply_snapshot(snap)
        self.log("restaurar", "backup", tr("Restaurou um backup da configuração") + (tr(" (mesclando)") if r else tr(" (substituindo)")), {"antes": antes})
        self.refresh_usage()

    def toggle_hide(self):
        i = self.cur()
        if not i: return
        o, was = self.usr["ocultos"], i["name"] in self.usr["ocultos"]
        o.remove(i["name"]) if was else o.append(i["name"])
        self.log("ocultar", i["name"], tr("Mostrou de novo: {n}" if was else "Ocultou: {n}", n=i["name"]), {"antes": was})
        self.refresh()

    def add_manual(self):
        """Add a program/script the scan did not find (exe, bat, cmd, ps1, py, jar, lnk)."""
        p = filedialog.askopenfilename(parent=self, title=tr("Escolha o arquivo que abre o programa"),
                                       filetypes=[(tr("Programas e scripts"), "*.exe *.bat *.cmd *.ps1 *.py *.jar *.lnk"),
                                                  (tr("Todos os arquivos"), "*.*")])
        if not p: return
        p = os.path.normpath(p)
        folder = os.path.dirname(p)
        name = simpledialog.askstring(tr("Adicionar"), tr("Nome do programa:"), initialvalue=Path(folder).name if
                                      Path(p).stem.lower() in ("run", "start", "launch", "main", "app") else Path(p).stem, parent=self)
        if not name or not name.strip(): return
        name = name.strip()
        if any(x["name"] == name for x in self.items):
            messagebox.showinfo(tr("Adicionar"), tr("Já existe um item com esse nome."), parent=self); return
        desc = simpledialog.askstring(tr("Adicionar"), tr("Para que serve (opcional):"), parent=self) or ""
        try: size = os.path.getsize(p)
        except OSError: size = None
        it = {"name": name, "lnk": "", "target": p, "ver": "", "company": "", "product": "", "desc": "", "manual": True,
              "location": folder, "size": size, "purpose": desc.strip() or f"Adicionado por você ({os.path.basename(p)}).",
              "category": "Programas sem instalador", "sub": "Adicionados por mim"}
        self.usr["manuais"].append(it)
        self.log("adicionar", name, tr("Adicionou à lista: {n}", n=name), {"remover": name})
        self.cur_cat = "__all__"; self.q.set(""); self.refresh()

    def remove_manual(self):
        i = self.cur()
        if not i or not i.get("manual"): return
        if not messagebox.askyesno(tr("Remover"), tr("Remover «{n}» da lista?\n(Os arquivos do programa não são tocados; dá para desfazer.)", n=i["name"]), parent=self):
            return
        self.usr["manuais"] = [m for m in self.usr["manuais"] if m["name"] != i["name"]]
        self.log("remover", i["name"], tr("Removeu da lista: {n}", n=i["name"]), {"item": i})
        self.refresh()

    def ps_trash(self, path):
        ps = ("Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::"
              f"DeleteFile({psq(path)},'OnlyErrorDialogs','SendToRecycleBin')")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], creationflags=NOWIN, stdin=subprocess.DEVNULL)

    def trash_lnk(self):
        i = self.cur()
        if not i or not i.get("lnk"): return
        lnk = i["lnk"]
        if not messagebox.askyesno(tr("Atalho quebrado"), tr("Enviar este atalho para a Lixeira?\n\n{p}\n\n"
                                   "Uma cópia fica guardada e você poderá desfazer (Ctrl+Z).", p=lnk)):
            return
        try:
            BACKUP.mkdir(parents=True, exist_ok=True)
            bk = BACKUP / f"{time.strftime('%Y%m%d-%H%M%S')}_{Path(lnk).name}"
            shutil.copy2(lnk, bk)
        except OSError as e:
            messagebox.showerror(tr("Erro"), tr("Não consegui guardar a cópia de segurança:\n{e}", e=e))
            return
        self.ps_trash(lnk)

        def finish(*_):
            if os.path.exists(lnk):
                messagebox.showerror(tr("Erro"), tr("O atalho não pôde ser removido."), parent=self)
                bk.unlink(missing_ok=True)
                return
            self.data["items"] = [x for x in self.scan_items if x is not i]
            self.save_idx()
            self.log("lixeira", i["name"], tr("Enviou o atalho quebrado à Lixeira: {n}", n=i["name"]),
                     {"backup": str(bk), "orig": lnk, "item": i})
            self.refresh()
        if os.path.exists(lnk):
            if messagebox.askyesno(tr("Sem permissão"), tr("O Windows não deixou remover o atalho (pasta de todos os usuários).\n"
                                   "Tentar como administrador (pedirá confirmação/senha)?"), parent=self):
                self.run_admin("Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::"
                               f"DeleteFile({psq(lnk)},'OnlyErrorDialogs','SendToRecycleBin')", finish)
            else:
                bk.unlink(missing_ok=True)
            return
        finish()

    def uninstall(self):
        i = self.cur()
        if not i:
            messagebox.showinfo(tr("Desinstalar"), tr("Selecione um programa na lista."), parent=self); return
        if i.get("broken"):
            messagebox.showinfo(tr("Desinstalar"), tr("Este atalho está quebrado: o programa já não existe.\n"
                                "Use o botão direito > Enviar atalho quebrado para a Lixeira."), parent=self); return
        if i.get("launcher") or i.get("manual"):
            messagebox.showinfo(tr("Desinstalar"), tr("Este programa abre por um arquivo/pasta (portátil), sem desinstalador.\n"
                                "Para removê-lo, use 'Abrir pasta' e apague a pasta pelo Explorer (vai para a Lixeira).\n"
                                "Se quiser só tirá-lo desta lista, use botão direito > Ocultar."), parent=self); return
        cmd = i.get("uninstall")
        if not cmd:
            if messagebox.askyesno(tr("Desinstalar"), tr("Não encontrei um desinstalador registrado para este item "
                                   "(pode ser um programa portátil).\n\nAbrir 'Aplicativos instalados' do Windows?"), parent=self):
                os.startfile("ms-settings:appsfeatures")
            return
        reg = i.get("uninstall_nome") or i["name"]
        aviso = ""
        if norm(reg) not in norm(i["name"]) and norm(i["name"]) not in norm(reg):
            aviso = tr("\n⚠ O desinstalador pertence a «{reg}», que é maior ou diferente de «{n}». "
                     "Isso remove o conjunto inteiro, não só este atalho.\n", reg=reg, n=i["name"])
        if not messagebox.askyesno(tr("Desinstalar"), tr("Desinstalar «{reg}»?\n{aviso}\n"
                                   "Será executado o desinstalador do Windows para este programa e o sistema vai pedir "
                                   "confirmação de administrador (senha).\n\n"
                                   "Comando:\n{cmd}\n\n"
                                   "ATENÇÃO: o app não consegue reverter uma desinstalação.", reg=reg, aviso=aviso, cmd=cmd), icon="warning", parent=self):
            return
        rp = messagebox.askyesnocancel(tr("Ponto de restauração"), tr("Criar um ponto de restauração do Windows antes de desinstalar?\n\n"
                                       "Sim = cria (permite voltar atrás pelo Windows; exige a Proteção do Sistema ativada; "
                                       "se não conseguir, a desinstalação é cancelada)\n"
                                       "Não = desinstala sem ponto de restauração\nCancelar = não fazer nada"), parent=self)
        if rp is None:
            return
        st = Path(tempfile.gettempdir()) / "appmanager_restore_status.txt"
        st.unlink(missing_ok=True)
        lines = ["$ErrorActionPreference='Stop'"]
        if rp:
            lines.append(f"try {{ Checkpoint-Computer -Description {psq(APP_NAME + ': antes de desinstalar ' + reg)} "
                         f"-RestorePointType APPLICATION_UNINSTALL; 'OK' | Set-Content {psq(str(st))} }} "
                         f"catch {{ ('FALHA: ' + $_.Exception.Message) | Set-Content {psq(str(st))}; exit 1 }}")
        lines.append(f"Start-Process cmd.exe -ArgumentList '/c', ('\"' + {psq(cmd)} + '\"') -Wait")

        def done(rc):
            status = st.read_text(encoding="utf-8-sig", errors="ignore").strip() if st.exists() else ""
            if rp and not status.startswith("OK"):
                messagebox.showwarning(tr("Desinstalar"), tr("Não foi possível criar o ponto de restauração, então nada foi desinstalado."
                                       "\n{status}\n\nSe quiser prosseguir sem ele, tente de novo e responda Não.", status=status), parent=self)
                return
            if rc not in (0, None) and not rp:
                messagebox.showinfo(tr("Desinstalar"), tr("A elevação foi cancelada ou falhou; nada foi desinstalado."), parent=self)
                return
            self.log("desinstalar", i["name"], tr("Executou o desinstalador de «{reg}»", reg=reg) +
                     (tr(" (com ponto de restauração do Windows)") if rp else ""), None)
            if messagebox.askyesno(tr("Desinstalar"), tr("O desinstalador foi executado.\nReescanear agora para atualizar a lista?"), parent=self):
                self.rescan()
        self.run_admin("\n".join(lines), done)

    def menu(self, e):
        if self.tab.identify_region(e.x, e.y) == "heading":
            return self.col_menu(e)
        r = self.tab.identify_row(e.y)
        if not r: return
        self.tab.selection_set(r)
        i = self.cur()
        m = tk.Menu(self, tearoff=0)
        m.add_command(label=tr("Abrir"), command=self.open_prog)
        m.add_command(label=tr("Abrir pasta"), command=self.open_dir)
        m.add_command(label=tr("Remover dos favoritos") if i["name"] in self.usr["favoritos"] else tr("Adicionar aos favoritos"),
                      command=self.toggle_fav)
        m.add_command(label=tr("Editar descrição…"), command=self.edit_desc)
        m.add_command(label=tr("Notas e tags…"), command=self.edit_notes)
        if i["name"] in self.upd:
            m.add_command(label=tr("Atualizar para {v} (winget)…", v=self.upd[i["name"]]["nova"]), command=self.update_prog)
        if len(i.get("variants", [])) > 1:
            vm = tk.Menu(m, tearoff=0)
            for v in i["variants"]:
                vm.add_command(label=os.path.basename(v), command=lambda v=v: self.open_prog(v))
            m.add_cascade(label=tr("Abrir variante"), menu=vm)
        m.add_command(label=tr("Desinstalar…"), command=self.uninstall, state="disabled" if i.get("broken") else "normal")
        m.add_command(label=tr("Mostrar de novo na lista") if i["name"] in self.usr["ocultos"] else tr("Ocultar da lista"),
                      command=self.toggle_hide)
        if i.get("manual"):
            m.add_command(label=tr("Remover item adicionado por mim…"), command=self.remove_manual)
        sub = tk.Menu(m, tearoff=0)
        cats = {}
        for x in self.items:
            if x["category"] != "Atalhos quebrados":
                cats.setdefault(x["category"], set()).add(self.sub(x))
        for c in sorted(cats | {"Outros": {"Geral"}}, key=lambda c: trc(c).lower()):
            cm = tk.Menu(sub, tearoff=0)
            for s in sorted(cats.get(c, {"Geral"}), key=lambda s: trc(s).lower()):
                cm.add_command(label=trc(s), command=lambda c=c, s=s: self.recat(c, s))
            cm.add_separator()
            cm.add_command(label=tr("Nova subcategoria…"), command=lambda c=c: self.recat(c, None))
            sub.add_cascade(label=trc(c), menu=cm)
        sub.add_separator()
        sub.add_command(label=tr("Nova categoria…"), command=lambda: self.recat(None, None))
        m.add_cascade(label=tr("Mover para categoria"), menu=sub)
        if i.get("broken"):
            m.add_separator(); m.add_command(label=tr("Enviar atalho quebrado para a Lixeira…"), command=self.trash_lnk)
        m.tk_popup(e.x_root, e.y_root)

    def recat(self, c, s):
        i = self.cur()
        if not i: return
        if c is None:
            c = simpledialog.askstring(tr("Nova categoria"), tr("Nome da categoria:"), parent=self)
            if not c or not c.strip(): return
            c = c.strip()
        if s is None:
            s = simpledialog.askstring(tr("Subcategoria"), tr("Subcategoria dentro de {c}:", c=trc(c)), parent=self)
            if not s or not s.strip(): return
            s = s.strip()
        cfg = config.load_local()
        ov = cfg.setdefault("overrides", {})
        antes = dict(over=ov.get(i["name"]), cat=i["category"], sub=i.get("sub", "Geral"))
        ov[i["name"]] = f"{c} > {s}"
        config.save_local(cfg)
        i["category"], i["sub"] = c, s
        self.save_idx()
        self.log("categoria", i["name"], tr("Moveu {n} para {c} › {s}", n=i["name"], c=trc(c), s=trc(s)), antes)
        self.cur_cat = "__all__" if self.cur_cat.startswith("__") else self.cur_cat
        self.refresh()

    # ---------- export ----------
    def export(self):
        path = filedialog.asksaveasfilename(parent=self, defaultextension=".csv", initialfile=tr("programas"),
                                            filetypes=[("CSV (Excel)", "*.csv"), (tr("Página HTML"), "*.html")])
        if not path: return
        rows = [(trc(i["category"]), trc(self.sub(i)), i["name"], i.get("ver") or "", fmt(i.get("size")), disk_of(i),
                 i.get("location", ""), i.get("company") or "", trd(self.purpose(i))) for i in self.filtered()]
        head = tuple(tr(h) for h in ("Categoria", "Subcategoria", "Nome", "Versão", "Tamanho", "Disco", "Local", "Fabricante", "Para que serve"))
        if path.lower().endswith(".html"):
            body = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)
            doc = ("<!doctype html><meta charset=utf-8><title>" + tr("Programas instalados") + "</title><style>"
                   "body{font:14px system-ui;margin:20px}table{border-collapse:collapse;width:100%}"
                   "td,th{border:1px solid #8884;padding:4px 8px;text-align:left}th{background:#8882}</style>"
                   "<h1>" + tr("Programas instalados") + "</h1><input id=f placeholder=\"" + tr("Buscar") + "\" oninput=\"for(const r of "
                   "document.querySelectorAll('tbody tr'))r.hidden=!r.textContent.toLowerCase().includes(this.value.toLowerCase())\">"
                   "<table><thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead><tbody>" + body + "</tbody></table>")
            Path(path).write_text(doc, encoding="utf-8")
        else:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f, delimiter=";"); w.writerow(head); w.writerows(rows)
        messagebox.showinfo(tr("Exportar"), tr("{n} programas exportados (respeitando busca e filtros atuais).", n=len(rows)))

    # ---------- rescan ----------
    def rescan(self):
        if self.proc and self.proc.poll() is None:
            return
        self.status.config(text=tr("Escaneando…"))
        self.proc = subprocess.Popen(([sys.executable, "--scan"] if getattr(sys, "frozen", False) else [sys.executable, str(RES / "scan.py")]),
                                     creationflags=NOWIN, stdin=subprocess.DEVNULL, env=self_env(),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.after(1500, self.poll)

    def poll(self):
        self.load()
        if self.proc and self.proc.poll() is None:
            self.after(1500, self.poll)
        else:
            self.proc = None
            self.load(force=True)

    # ---------- help (renders help/<language>.md) ----------
    def show_help(self):
        if self.help_win and self.help_win.winfo_exists():
            self.help_win.deiconify(); self.help_win.lift(); self.help_win.focus_set()
            return
        w = self.help_win = tk.Toplevel(self)
        self.after_idle(self.center, w)
        w.title(tr("Ajuda — {app}", app=APP_NAME)); w.geometry("820x680"); w.transient(self)
        w.bind("<Escape>", lambda e: w.destroy())
        bar = ttk.Frame(w); bar.pack(side="top", fill="x", padx=8, pady=6)
        ttk.Button(bar, text=tr("Ir ao índice"), command=lambda: self.help_txt.yview("m_" + slug(tr("Índice")))).pack(side="left")
        ttk.Button(bar, text=tr("Abrir arquivo de ajuda"), command=lambda: HELP.exists() and os.startfile(HELP)).pack(side="left", padx=6)
        ttk.Button(bar, text=tr("Fechar"), command=w.destroy).pack(side="right")
        t = self.help_txt = tk.Text(w, wrap="word", relief="flat", padx=18, pady=12, font=("Segoe UI", 10), spacing3=3)
        sb = ttk.Scrollbar(w, command=t.yview); t.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y"); t.pack(side="left", fill="both", expand=True)
        for tag, kw in (("h1", dict(font=("Segoe UI", 16, "bold"), spacing3=6)),
                        ("h2", dict(font=("Segoe UI", 13, "bold"), spacing1=14, spacing3=6)),
                        ("h3", dict(font=("Segoe UI", 11, "bold"), spacing1=8, spacing3=4)),
                        ("b", dict(font=("Segoe UI", 10, "bold"))), ("code", dict(font=("Consolas", 10))),
                        ("li", dict(lmargin1=18, lmargin2=34)), ("quote", dict(lmargin1=14, lmargin2=14, font=("Segoe UI", 10, "italic"))),
                        ("link", dict(underline=True))):
            t.tag_config(tag, **kw)
        self.render_md(t, HELP.read_text(encoding="utf-8") if HELP.exists() else "# " + tr("Ajuda") + "\n\n" + tr("O arquivo de ajuda não foi encontrado."))
        t.config(state="disabled")
        self.style_help()

    def render_md(self, t, md):
        inline = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\(#[^)]+\))")

        def put(text, base=()):
            for part in inline.split(text):
                if not part: continue
                if part.startswith("**"): t.insert("end", part[2:-2], base + ("b",))
                elif part.startswith("`"): t.insert("end", part[1:-1], base + ("code",))
                elif part.startswith("["):
                    label, target = re.match(r"\[([^\]]+)\]\(#([^)]+)\)", part).groups()
                    tg = "lk_" + target
                    t.insert("end", label, base + ("link", tg))
                    t.tag_bind(tg, "<Button-1>", lambda e, m="m_" + target: t.yview(m))
                    t.tag_bind(tg, "<Enter>", lambda e: t.config(cursor="hand2"))
                    t.tag_bind(tg, "<Leave>", lambda e: t.config(cursor=""))
                else: t.insert("end", part, base)
        for raw in md.splitlines():
            ln = raw.rstrip()
            m = re.match(r"^(#{1,3})\s+(.*)", ln)
            if m:
                t.mark_set("m_" + slug(m.group(2)), "end-1c"); t.mark_gravity("m_" + slug(m.group(2)), "left")
                t.insert("end", m.group(2) + "\n", f"h{len(m.group(1))}")
            elif re.match(r"^\s*([-*])\s+", ln):
                t.insert("end", "• ", ("li",)); put(re.sub(r"^\s*[-*]\s+", "", ln), ("li",)); t.insert("end", "\n")
            elif re.match(r"^\s*\d+\.\s+", ln):
                n, rest = re.match(r"^\s*(\d+\.)\s+(.*)", ln).groups()
                t.insert("end", n + " ", ("li",)); put(rest, ("li",)); t.insert("end", "\n")
            elif ln.startswith(">"):
                put(ln.lstrip("> "), ("quote",)); t.insert("end", "\n")
            elif ln.strip() in ("---", "***"):
                t.insert("end", "─" * 60 + "\n")
            elif ln.strip():
                put(ln); t.insert("end", "\n")
            else:
                t.insert("end", "\n")

    def style_help(self):
        if not (self.help_win and self.help_win.winfo_exists()):
            return
        p = DARK if self.dark else LIGHT
        self.help_win.configure(bg=p["bg"])
        self.help_txt.config(bg=p["field"], fg=p["fg"])
        self.help_txt.tag_config("link", foreground=p["link"])
        self.help_txt.tag_config("code", background=p["head"])
        self.help_txt.tag_config("quote", foreground=p["link"])


if __name__ == "__main__":
    if "--scan" in sys.argv:                  # in the .exe, rescanning runs the program itself with --scan
        import scan
        scan.main()
    else:
        if getattr(sys, "frozen", False):        # .exe without console: errors go to erro.log (next to the .exe)
            try:
                sys.stderr = open(BASE / "erro.log", "a", encoding="utf-8", buffering=1)
            except OSError:
                sys.stderr = open(os.devnull, "w")
            if sys.stdout is None:
                sys.stdout = open(os.devnull, "w")
        App().mainloop()
