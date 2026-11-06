"""Idiomas da interface (padrão: English). Os textos-fonte do código estão em português; os arquivos lang/en.json e lang/es.json
traduzem: "ui" (botões, menus, mensagens), "cat" (categorias e subcategorias), "desc" (descrições "para que serve")
e "patterns" (descrições geradas pelo scan, com trechos variáveis). Traduções privadas opcionais ficam em
lang.local.<idioma>.json (ao lado dos dados; ignorado pelo git). O idioma vale ao iniciar (a troca reinicia o app)."""
import json, re
from paths import APP, RES

LANGS = {"en": "English", "pt": "Português", "es": "Español"}
DEFAULT = "en"


def _read(p):
    try:
        d = json.loads(p.read_text(encoding="utf-8-sig"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _saved():
    return _read(APP / "user.json").get("idioma")


LANG = _saved() if _saved() in LANGS else DEFAULT
_T = {"ui": {}, "cat": {}, "desc": {}, "patterns": []}
if LANG != "pt":
    for src in (_read(RES / "lang" / f"{LANG}.json"), _read(APP / f"lang.local.{LANG}.json")):
        for k in ("ui", "cat", "desc"):
            _T[k].update(src.get(k, {}))
        _T["patterns"] += src.get("patterns", [])


def tr(s, **kw):
    """Traduz um texto da interface (a chave é o texto em português); {campos} são preenchidos com kw."""
    t = _T["ui"].get(s, s)
    return t.format(**kw) if kw else t


def trc(s):
    """Nome de categoria/subcategoria para exibição (nomes criados pelo usuário ficam como estão)."""
    return _T["cat"].get(s, s)


def trd(s):
    """Descrição 'para que serve' para exibição (exata, ou por padrão para as geradas pelo scan)."""
    if not s or LANG == "pt":
        return s
    if s in _T["desc"]:
        return _T["desc"][s]
    for pat, rep in _T["patterns"]:
        m = re.match(pat, s, re.S)
        if m:
            return rep.format(*[trd(g) for g in m.groups()])
    return s
