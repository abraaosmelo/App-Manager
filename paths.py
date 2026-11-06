"""Pastas do app. Rodando do código-fonte, tudo fica na pasta do projeto.
Rodando como .exe (PyInstaller), os recursos vão embutidos (RES) e os dados do usuário ficam ao lado do .exe (APP)."""
import os, sys
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)
RES = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))          # lang/, help/, assets/ e categories.json padrão
APP = Path(sys.executable).parent if FROZEN else Path(__file__).parent

# nomes antigos (versões em português) -> nomes atuais; os dados do usuário são renomeados na primeira execução
LEGACY = {"indice.json": "index.json", "usuario.json": "user.json", "atualizacoes.json": "updates.json",
          "categorias.json": "categories.json"}


def _writable(p):
    try:
        t = p / ".write-test.tmp"
        t.write_text("x"); t.unlink()
        return True
    except OSError:
        return False


if FROZEN and not _writable(APP):                                     # ex.: .exe em Program Files
    APP = Path(os.environ.get("APPDATA", str(Path.home()))) / "App-Manager"
    APP.mkdir(parents=True, exist_ok=True)


def migrate():
    """Renomeia os arquivos antigos. Se os dois existem, vale o mais recente (uma versão antiga pode ter gravado depois)."""
    for old, new in LEGACY.items():
        o, n = APP / old, APP / new
        try:
            if o.exists() and (not n.exists() or o.stat().st_mtime > n.stat().st_mtime):
                os.replace(o, n)
        except OSError:
            pass


migrate()
