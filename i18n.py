"""Interface languages (default: English). The source texts in the code are in Portuguese; the files lang/en.json, lang/es.json,
lang/fr.json and lang/de.json translate them: "ui" (buttons, menus, messages), "cat" (categories and subcategories), "desc" ("what it does" descriptions)
and "patterns" (scan-generated descriptions, with variable parts). Optional private translations live in
lang.local.<language>.json (next to the data; ignored by git). The language applies at startup (changing it restarts the app)."""
import json, re
from paths import APP, RES

LANGS = {"en": "English", "pt": "Português", "es": "Español", "fr": "Français", "de": "Deutsch"}
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
    """Translate a UI text (the key is the Portuguese text); {fields} are filled in with kw."""
    t = _T["ui"].get(s, s)
    return t.format(**kw) if kw else t


def trc(s):
    """Category/subcategory name for display (user-created names stay as they are)."""
    return _T["cat"].get(s, s)


def trd(s):
    """'What it does' description for display (exact match, or by pattern for scan-generated ones)."""
    if not s or LANG == "pt":
        return s
    if s in _T["desc"]:
        return _T["desc"][s]
    for pat, rep in _T["patterns"]:
        m = re.match(pat, s, re.S)
        if m:
            return rep.format(*[trd(g) for g in m.groups()])
    return s
