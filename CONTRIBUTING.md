# Contributing to App-Manager

Thanks for your interest! App-Manager is a small hobby project: a Tkinter app (Python standard library only) that catalogs the programs installed on Windows. It was built in spare time with AI assistance ([Claude Code](https://claude.com/claude-code)), and improvements from humans are very welcome, whatever your level.

## Ideas to start with

- **A new language**: copy `lang/en.json` to `lang/<code>.json`, translate the values, and add the code to `LANGS` in `i18n.py` and a `help/<code>.md`. Spanish and Portuguese are the examples to follow.
- **More catalog entries**: add common programs to `categories.json` (name words → category, subcategory, description) and their translations in `lang/*.json`. Only generic, widely used software, never personal or niche apps.
- **Polish the UI**: for example, the *Last used* column truncates long texts such as "7 month(s) ago"; better dark/light details; keyboard navigation.
- **Quality**: unit tests for `usage.py` (winget table parsing) and `scan.py`, a lint/CI workflow on GitHub Actions.
- **Distribution**: a signed `.exe` or an installer, a `winget`/Scoop manifest.
- **Test on your machine** (other Windows versions, languages, winget output) and open an issue with what you find.

## How to run

```
git clone https://github.com/thomasmeneghelli/App-Manager.git
cd App-Manager
App-Manager.bat        (or: python scan.py, then pythonw app.py)
```

Windows 10/11 and Python 3 with Tkinter. No extra dependencies.

## Rules of the project

1. **Texts go through `tr("texto em português")`** (`i18n.py`). The Portuguese text is the key; add the English and Spanish translations in `lang/en.json` and `lang/es.json`.
2. **Update the Help** (`help/pt.md`, `help/en.md`, `help/es.md`) when you change menus, buttons, shortcuts or behavior, including the index at the top.
3. **Never commit personal data**: `index.json`, `user.json`, `updates.json`, `icons/`, `backup/`, `categories.local.json`, `lang.local.*.json` are git-ignored. Screenshots must use made-up data.
4. **Never run an uninstall while testing**; test up to the confirmation dialog.
5. Keep it simple: standard library only, small functions, no new dependency without a good reason.

More details for contributors are in [`CLAUDE.md`](CLAUDE.md) (project structure and conventions).

## Sending changes

1. Fork, create a branch, make a focused change.
2. Check it by running the app (and the language you touched).
3. Open a pull request saying what changed and why. Small PRs are easier to review.

Not a programmer? Opening an [issue](https://github.com/thomasmeneghelli/App-Manager/issues) with a bug, an idea or a translation fix is a real contribution too.
