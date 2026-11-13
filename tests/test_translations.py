"""Consistency checks for the translations (lang/*.json) and the Help (help/*.md).

They catch a text added with tr("...") but not translated, a translation that lost a {field},
a catalog description without translation and a Help index link without a matching section.

Run from the project folder:  python -m unittest discover -s tests
"""
import ast
import json
import re
import string
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANGS = [p.stem for p in sorted((ROOT / "lang").glob("*.json"))]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def code_strings():
    """(tr keys, all string constants) found in the project's .py files.

    A tr key is the literal first argument of tr(...), including both branches of `a if c else b`.
    Keys built at runtime (tr(name) over a list of literals) are covered by the cross-language check.
    """
    keys, consts = {}, set()
    for f in sorted(ROOT.glob("*.py")):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                consts.add(n.value)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "tr" and n.args:
                args = [n.args[0]]
                while args:
                    a = args.pop()
                    if isinstance(a, ast.IfExp):
                        args += [a.body, a.orelse]
                    elif isinstance(a, ast.Constant) and isinstance(a.value, str):
                        keys.setdefault(a.value, f"{f.name}:{n.lineno}")
    return keys, consts


def fields(s):
    """Names of the {fields} in a format string."""
    return sorted(f for _, f, _, _ in string.Formatter().parse(s) if f is not None)


def slug(s):
    # Same as app.slug (kept here so the test does not import the Tk app).
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


KEYS, CONSTS = code_strings()
CATALOG = load(ROOT / "categories.json")
CAT_NAMES = ({e["c"] for e in CATALOG["catalogo"]} | {e["s"] for e in CATALOG["catalogo"] if e.get("s")}
             | set(CATALOG["regras"]))
DESCS = {e["d"] for e in CATALOG["catalogo"] if e.get("d")}


class TranslationsTest(unittest.TestCase):

    def test_languages_match_i18n(self):
        """Every lang/<code>.json is listed in i18n.LANGS, and every language but Portuguese has a file."""
        tree = ast.parse((ROOT / "i18n.py").read_text(encoding="utf-8"))
        langs = next(ast.literal_eval(n.value) for n in tree.body
                     if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "LANGS")
        self.assertEqual(sorted(set(langs) - {"pt"}), LANGS)

    def test_every_tr_text_is_translated(self):
        for lang in LANGS:
            ui = load(ROOT / "lang" / f"{lang}.json")["ui"]
            missing = [f"{k!r} ({where})" for k, where in KEYS.items() if k not in ui]
            with self.subTest(lang=lang):
                self.assertEqual(missing, [], f"lang/{lang}.json 'ui' is missing these tr() texts")

    def test_languages_have_the_same_ui_keys(self):
        """Catches texts translated in one language only (e.g. keys built at runtime)."""
        sets = {lang: set(load(ROOT / "lang" / f"{lang}.json")["ui"]) for lang in LANGS}
        every = set().union(*sets.values())
        for lang, keys in sets.items():
            with self.subTest(lang=lang):
                self.assertEqual(sorted(every - keys), [], f"lang/{lang}.json 'ui' is missing keys other languages have")

    def test_fields_are_kept(self):
        for lang in LANGS:
            ui = load(ROOT / "lang" / f"{lang}.json")["ui"]
            bad = [k for k, v in ui.items() if fields(k) != fields(v)]
            with self.subTest(lang=lang):
                self.assertEqual(bad, [], f"lang/{lang}.json: translation has different {{fields}} than the key")

    def test_no_stale_keys(self):
        """A key no longer in the code or the catalog is a leftover from a removed text."""
        for lang in LANGS:
            d = load(ROOT / "lang" / f"{lang}.json")
            with self.subTest(lang=lang):
                self.assertEqual([k for k in d["ui"] if k not in CONSTS], [], "ui")
                self.assertEqual([k for k in d["cat"] if k not in CAT_NAMES and k not in CONSTS], [], "cat")
                self.assertEqual([k for k in d["desc"] if k not in DESCS], [], "desc")

    def test_catalog_descriptions_are_translated(self):
        for lang in LANGS:
            desc = load(ROOT / "lang" / f"{lang}.json")["desc"]
            with self.subTest(lang=lang):
                self.assertEqual(sorted(DESCS - set(desc)), [], f"lang/{lang}.json 'desc' is missing catalog descriptions")

    def test_patterns(self):
        """Each pattern compiles and its replacement uses one {} per captured group."""
        for lang in LANGS:
            for pat, rep in load(ROOT / "lang" / f"{lang}.json")["patterns"]:
                with self.subTest(lang=lang, pattern=pat):
                    self.assertEqual(re.compile(pat).groups, len(fields(rep)))


class HelpTest(unittest.TestCase):

    def test_help_exists_for_every_language(self):
        self.assertEqual(sorted(p.stem for p in (ROOT / "help").glob("*.md")), sorted(LANGS + ["pt"]))

    def test_index_links_match_sections(self):
        """The index lists every section, in order, and each link reaches a heading (same slug rule as the app)."""
        for md in sorted((ROOT / "help").glob("*.md")):
            text = md.read_text(encoding="utf-8")
            heads = [slug(h) for h in re.findall(r"^#{1,3}\s+(.*?)\s*$", text, re.M)]
            index = text.split("\n## ", 2)[1] if text.count("\n## ") >= 2 else ""
            links = re.findall(r"\]\(#([^)]+)\)", index)
            with self.subTest(help=md.name):
                self.assertTrue(links, "no index found")
                self.assertEqual([l for l in links if l not in heads], [], "links without a matching heading")
                body = [h for h in heads[2:] if h in links]
                self.assertEqual(body, links, "index order differs from the sections")

    def test_index_heading_matches_go_to_index_button(self):
        """The "Ir ao índice" button jumps to the heading named tr("Índice")."""
        for lang in LANGS + ["pt"]:
            name = "Índice" if lang == "pt" else load(ROOT / "lang" / f"{lang}.json")["ui"]["Índice"]
            text = (ROOT / "help" / f"{lang}.md").read_text(encoding="utf-8")
            with self.subTest(lang=lang):
                self.assertRegex(text, rf"(?m)^#{{1,3}}\s+{re.escape(name)}\s*$")


if __name__ == "__main__":
    unittest.main()
