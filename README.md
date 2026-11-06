<p align="center"><img src="assets/logo-256.png" alt="App-Manager" width="128"></p>

# App-Manager

**English** · [Português](README.pt.md) · [Español](README.es.md)

A catalog of the programs installed on **Windows**: what each one does, when you last used it, how much space it takes, its category, and buttons to open, update or uninstall it. Plain Python + Tkinter, no external dependencies, everything runs locally. The interface is in **English by default**, with **Português** and **Español** one click away (menu 🌐 *Language*).

## Requirements

| | |
|---|---|
| System | **Windows 10 / 11** (uses the registry, the Start Menu and `winget`; not for Linux/macOS) |
| `.exe` version | Nothing besides Windows |
| Python version | Python 3 with Tkinter and `python`/`pythonw` on PATH (tested on Python 3.15 and Windows 11); standard library only |
| Optional | [`winget`](https://learn.microsoft.com/windows/package-manager/winget/) for the update column and menu |

## Install and run

**Option A — `.exe` (no Python needed):**
1. Download `App-Manager.exe` from [Releases](https://github.com/thomasmeneghelli/App-Manager/releases).
2. Put it in a folder you can write to (e.g. `D:\Apps\App-Manager`) and double-click it. It creates its data files next to it.
3. The first run scans your PC (1–2 min). Windows SmartScreen may warn you, because the `.exe` has no digital signature.

**Option B — Python:**
1. Install [Python](https://www.python.org/downloads/) and tick **Add python.exe to PATH**.
2. Download this repository (**Code → Download ZIP**, or `git clone https://github.com/thomasmeneghelli/App-Manager.git`).
3. Double-click **`App-Manager.bat`**.

To build the `.exe` yourself: `build_exe.bat`. **F1** opens the in-app Help.

## Features

- Reads the Start Menu shortcuts and the Windows registry; also finds programs launched by `.bat`/`.cmd` files.
- Categories and subcategories, a "what it does" description, filters by disk and size, search (including your notes and tags).
- **Last used**, times used and install date columns (read from the Windows UserAssist).
- Ready-made lists: favorites, most used, cleanup suggestions, start with Windows, with update, duplicate versions.
- **Update** through winget and **Uninstall** through the Windows uninstaller (asks for the UAC password).
- **Undo**, action history, configuration backup, a summary with charts and CSV/HTML export.
- Menus **File, View, Tools, Language and Help**, light/dark theme and shortcuts (`F1`, `F5`, `Ctrl+F`, `Ctrl+E`, `Ctrl+Z`).

## Privacy and safety

- Everything runs on your machine; nothing is sent to the internet (only `winget`, if you ask for updates).
- The scan and the registry reads are **read-only**.
- Updating and uninstalling **cannot be undone** by the app; it asks for confirmation first. Use at your own risk.
- Your data (`user.json`, `index.json`, `updates.json`, `icons/`, `backup/`, `categories.local.json`) is created locally and ignored by git. The repository ships only a generic catalog of common programs.

## Customize

Add your own programs and descriptions in `categories.local.json` (optional, same format as `categories.json`; your entries win), then rescan. Translations live in `lang/`. Full help: [English](help/en.md), [Português](help/pt.md), [Español](help/es.md).

## Files

| File | Purpose |
|---|---|
| `App-Manager.bat` | Opens the app (runs the first scan if needed) |
| `app.py` | Main window |
| `scan.py` | Program scan, sizes and uninstallers |
| `usage.py` | Usage, startup, winget and duplicate-version reads |
| `config.py` | Merges `categories.json` with your private `categories.local.json` |
| `i18n.py`, `lang/` | Languages (en, pt, es) |
| `paths.py`, `version.py` | Data/resource folders and app identity |
| `categories.json` | Default catalog and rules |
| `help/` | Full help (also shown in the app) |
| `assets/`, `tools/make_logo.py` | Logo, icon and their generator |
| `build_exe.bat` | Builds the portable `.exe` (PyInstaller) |

## License

[MIT](LICENSE)
