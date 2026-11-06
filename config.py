"""Configuração do catálogo de programas.

- categories.json: catálogo padrão (versionado; no .exe vem embutido).
- categories.local.json: o SEU catálogo (privado, ignorado pelo git): entradas extras, categorias movidas ("overrides"),
  pastas extras para procurar .bat ("launchers") e "limpeza_dias". As entradas locais vencem as do catálogo padrão."""
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
    """Catálogo mesclado (padrão + local)."""
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
