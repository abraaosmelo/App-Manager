"""Program catalog configuration.

- categories.json: default catalog (versioned; bundled inside the .exe).
- categories.local.json: YOUR catalog (private, ignored by git): extra entries, moved categories ("overrides"),
  extra folders to look for .bat files ("launchers") and "limpeza_dias". Local entries win over the default catalog."""
import json
from paths import APP, RES

BASE_FILE = RES / "categories.json"
LOCAL_FILE = APP / "categories.local.json"


def _read(p):
    try:
        d = json.loads(p.read_text(encoding="utf-8-sig"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def load_local():
    return _read(LOCAL_FILE)


def save_local(cfg):
    LOCAL_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")


def load():
    """Merged catalog (default + local)."""
    base, local = _read(BASE_FILE), load_local()
    cfg = dict(base)
    cfg["catalogo"] = local.get("catalogo", []) + base.get("catalogo", [])
    regras = {k: list(v) for k, v in base.get("regras", {}).items()}
    for k, words in local.get("regras", {}).items():
        regras.setdefault(k, [])
        regras[k] += [w for w in words if w not in regras[k]]
    cfg["regras"] = regras
    for k in ("descricoes", "overrides"):
        cfg[k] = {**base.get(k, {}), **local.get(k, {})}
    cfg["launchers"] = {"raizes_extra": base.get("launchers", {}).get("raizes_extra", [])
                        + local.get("launchers", {}).get("raizes_extra", [])}
    for k in ("limpeza_dias",):
        if k in local or k in base:
            cfg[k] = local.get(k, base.get(k))
    return cfg
