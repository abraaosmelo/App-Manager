"""App folders. When running from source, everything lives in the project folder.
When running as an .exe (PyInstaller), resources are bundled (RES) and user data stays next to the .exe (APP)."""
import os, sys
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)
RES = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))          # lang/, help/, assets/ and the default categories.json
APP = Path(sys.executable).parent if FROZEN else Path(__file__).parent

# old names (Portuguese versions) -> current names; user data is renamed on first run
LEGACY = {"indice.json": "index.json", "usuario.json": "user.json", "atualizacoes.json": "updates.json",
          "categorias.json": "categories.json"}


def _writable(p):
    try:
        t = p / ".write-test.tmp"
        t.write_text("x"); t.unlink()
        return True
    except OSError:
        return False


if FROZEN and not _writable(APP):                                     # e.g. .exe in Program Files
    APP = Path(os.environ.get("APPDATA", str(Path.home()))) / "App-Manager"
    APP.mkdir(parents=True, exist_ok=True)


def migrate():
    """Rename the old files. If both exist, the newer one wins (an old version may have written later)."""
    for old, new in LEGACY.items():
        o, n = APP / old, APP / new
        try:
            if o.exists() and (not n.exists() or o.stat().st_mtime > n.stat().st_mtime):
                os.replace(o, n)
        except OSError:
            pass


migrate()
