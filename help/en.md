# App-Manager — Help

## Index

- [What it is](#what-it-is)
- [Browsing: categories and subcategories](#browsing-categories-and-subcategories)
- [Columns: last used, times used, installed on](#columns-last-used-times-used-installed-on)
- [Special categories](#special-categories)
- [Cleanup suggestions](#cleanup-suggestions)
- [Start with Windows](#start-with-windows)
- [Updates (winget)](#updates-winget)
- [Duplicate versions](#duplicate-versions)
- [Notes and tags](#notes-and-tags)
- [Summary](#summary)
- [Configuration backup](#configuration-backup)
- [Search and filter (disk, size)](#search-and-filter-disk-size)
- [Programs opened by .bat (portable)](#programs-opened-by-bat-portable)
- [Add and hide items](#add-and-hide-items)
- [Opening programs](#opening-programs)
- [Right-click menu](#right-click-menu)
- [Uninstall (asks for a password)](#uninstall-asks-for-a-password)
- [Undo and history](#undo-and-history)
- [Top menus](#top-menus)
- [Language](#language)
- [Keyboard shortcuts](#keyboard-shortcuts)
- [Portable .exe version](#portable-exe-version)
- [Files in the folder](#files-in-the-folder)
- [Tips and limits](#tips-and-limits)

## What it is

An index of the programs installed on this PC, built from the **Start Menu shortcuts** (and from a few programs in the Windows registry that have no shortcut). For each one it shows name, version, install location, size, disk, category and **what it does**.

To open it: double-click `App-Manager.bat` (or `App-Manager.exe` in the portable version; see "Portable .exe version").

The app only reads information. It changes something only when you ask: uninstall, send a broken shortcut to the Recycle Bin, move to another category, etc.

## Browsing: categories and subcategories

- **Left pane:** categories with the number of programs. Click the arrow to open the **subcategories** (for example, Development › Editors and IDEs).
- **Right pane:** list with icon, name, version, size, disk, category › subcategory and location. Click a column title to sort.
- **Footer:** details of the selected item (category, disk, version, publisher, how many times it was opened from here, size, location, whether there is an uninstaller and what it does).
- **Status bar** (top right): total shown, "calculating sizes…", how long ago the last scan ran ("scanned 5 min ago"; if it is old, use Rescan), new and removed.

## Columns: last used, times used, installed on

The table has these columns (**right-click a column title** to show or hide it; there is "Restore default columns"; the table scrolls horizontally if it does not fit): Name, Version, Update, Size, Disk, **Last used**, **Times used**, **Installed on**, Starts with Windows, Tags, Category › Subcategory and Location. Click a title to sort.

- **Last used and Times used:** come from the Windows registry (UserAssist), which records when you open a program from Explorer, the Start Menu, the taskbar or the desktop. They are added to the launches made through this index (the larger number wins, so nothing is counted twice). The data is read again every time you return to the window. The Last used column widens by itself to fit the longest text.
- **"no record"** means Windows did not note any launch. This **does not prove** the program was never used: Windows does not record programs opened from the command line, from `.bat` scripts, from services or from Task Manager, and the history only exists since the feature was turned on.
- **Installed on:** the install date from the Windows registry when it exists; otherwise the creation date of the program folder (which may be the date the folder was copied).

## Special categories

- **All:** everything that was found.
- **★ Favorites:** the programs you marked.
- **Most used:** the 15 most launched (Windows registry + this index).
- **New since last scan:** programs that appeared after the previous scan (marked "(new)").
- **No Start Menu shortcut:** installed programs that have no shortcut but have an executable that can be opened.
- **Cleanup suggestions, Start with Windows, With update and Duplicate versions:** see the sections below.
- **Tags:** appears when you create tags; each tag becomes a filter.
- **Hidden:** appears only when you have hidden some item (see "Add and hide items").
- **Broken shortcuts:** shortcuts whose program no longer exists (probably uninstalled). Its subcategories show the kind of program it was.

## Cleanup suggestions

Lists the programs **unused for 180 days or more, or with no usage record**, from largest to smallest, and the status bar shows how much space that could free up (folders counted once). Left out: the System category, broken shortcuts and your favorites.

It is only a suggestion. Since "no record" may be a program you use in other ways, check each item before using **Uninstall…**. To change the period, put `"limpeza_dias": 365` in `categories.local.json` and reopen the app.

## Start with Windows

Shows the programs that start by themselves when the PC boots, read from the registry *Run* keys and the Startup folder. The **Starts with Windows** column shows **Yes** or **Disabled** (when you already turned it off in Task Manager); the category lists only the active ones. The app only shows them: to turn them on or off, use the Startup tab in Task Manager. The link between the entry and the program is by executable path or install folder, so it may list several shortcuts of the same program.

## Updates (winget)

- **Tools › Check updates** queries Windows `winget` (about 15 s) and saves the result in `updates.json`.
- Items with a new version get the **Update** column (→ version), the **With update** category and a detail line. The **Update…** button (or right-click) runs `winget upgrade` in a console window, with confirmation; Windows may ask for the administrator password.
- The app **cannot undo** an update. When the winget window closes, the app checks winget again (without a message) and removes what was already updated from the list. For the Version column to show the new version, click Rescan.
- Only programs that winget knows and that match the item name appear; Windows components, drivers and Store apps are left out.

## Duplicate versions

The **Duplicate versions** category groups similar items, for example several Pythons, two Visual Studios or the "x86" and "x64" shortcuts. The detail shows the group and the total space. It helps you decide what to uninstall; not every group is a problem (shortcuts of the same program are included too).

## Notes and tags

**Notes and tags…** (footer button or right-click) opens a window to write notes (license, where you downloaded it, project) and comma-separated tags. Tags appear in the **Tags** category (one filter per tag) and in the Tags column; search also looks at notes and tags. It can be undone.

## Summary

The **Tools › Programs summary…** menu opens a screen with: number of programs and total space, cleanup suggestions, how many start with Windows and have an update, duplicate groups, space by category and by disk, the 10 largest, the 10 most used and installations per year. Hidden items and broken shortcuts are not counted.

## Configuration backup

**File › Save configuration backup…** saves to a `.json` file everything that is yours: favorites, usage count and date, edited descriptions, notes, tags, hidden items, added items, chosen columns and moved categories. **File › Restore backup…** asks whether to **merge** with what exists or **replace**; before that the app keeps a copy of the current state in `backup/`, and you can **undo** it from the History. Useful to take your setup to another PC or after reinstalling Windows.

## Search and filter (disk, size)

- **Search:** looks in name, description, location, category, subcategory, publisher, notes and tags (also in the translated names and descriptions, in the chosen language). The counts in the left pane adjust.
- **Disk:** lists only the programs installed on C:, D:, F: etc. (the letters appear according to your PC).
- **Size:** under 100 MB, over 100 MB, 500 MB, 1 GB or 5 GB. Programs whose size is still "…" (being calculated) are left out of these filters.
- **Clear filters** puts everything back to normal. Search and filters work together and also apply to **export**.

## Programs opened by .bat (portable)

Some programs have neither an installer nor a shortcut: you open a `run.bat` or `start.bat` inside the folder (common in portable and AI tools). The scan looks for these `.bat` and `.cmd` files and shows each **folder as one item**, in the **Programs without installer** category (or in another category, if the catalog knows the program).

- **Where it looks:** Downloads, Desktop, Documents and the disks other than the Windows one (D:, F:…), up to 3 or 4 folder levels deep. To include another folder, put the path in `categories.local.json`, under `"launchers": {"raizes_extra": ["E:\\Programs"]}`, and rescan.
- **Which files count:** startup names (`run`, `start`, `launch`, `iniciar`, `abrir`, `webui`…), or the only `.bat` in a folder. It ignores installers, test and build scripts, and internal folders (`venv`, `node_modules`, `bin`, `python_embeded`…), as well as folders of programs that already appear through the Start Menu.
- **Variants:** if the folder has several launchers (`run.bat`, `run_anime.bat`…), the item opens the main one and right-click > **Open variant** lists the others.
- The `.bat` runs in its own folder, in a console window. Programs like this have no uninstaller: to remove one, use **Open folder** and delete the folder in Explorer.
- Things that are not really programs may show up (loose scripts, development tools). Use **Hide** in those cases.
- The scan takes longer (about 1 min 30 s) because of this search on the disks.

## Add and hide items

- **Add…** (footer button): choose an `.exe`, `.bat`, `.cmd`, `.ps1`, `.py`, `.jar` or `.lnk` that the scan did not find. Enter the name and, if you want, what it does. It goes into *Programs without installer › Added by me*. To remove it: right-click > **Remove item I added** (it does not delete the files).
- **Hide from the list** (right-click): hides an item from all screens and counts. Hidden items stay in the **Hidden** category, where right-click offers **Show in the list again**.
- Both can be undone (Ctrl+Z or History) and survive a rescan.

## Opening programs

- Double-click, `Enter` or the **Open** button: opens the program (through the Start Menu shortcut, when there is one; `.bat` scripts run in their own folder).
- **Open folder:** opens the install folder in Explorer.
- **★ Favorite:** marks or unmarks the selected item.

## Right-click menu

- **Open**, **Open folder**, **Add to / Remove from favorites**, **Open variant** (when the folder has several `.bat` files).
- **Hide from the list** / **Show in the list again** and **Remove item I added**: see "Add and hide items".
- **Notes and tags…**, and **Update to… (winget)** when there is a new version.
- **Edit description…:** replaces the "what it does" text (kept in `user.json`). Leave it blank to go back to the original.
- **Uninstall…:** see the section below.
- **Move to category:** choose the category and subcategory, or create new ones ("New subcategory…", "New category…"). It is saved in `categories.local.json` and applies to future scans.
- **Send broken shortcut to the Recycle Bin…:** only appears on broken shortcuts. It asks for confirmation, keeps a copy of the shortcut and sends it to the Recycle Bin (it is not deleted for good).

## Uninstall (asks for a password)

The **Uninstall…** button (or the right-click menu) uses the uninstaller that Windows itself has registered for the program.

1. The app shows the registered name and the command it will run, and asks for confirmation.
2. It asks whether you want to **create a Windows restore point** first. With it you can roll back through Windows (System Restore). It requires *System Protection* to be on; if it cannot be created, nothing is uninstalled.
3. Windows asks for **administrator confirmation (password)**, and the uninstaller runs.
4. When it finishes, the app offers to rescan the list.

> **Warning:** the app **cannot revert** an uninstall. The only way back is the Windows restore point or reinstalling the program.

Things to watch for:

- Several shortcuts may belong to the same program (for example, Word, Excel and Outlook belong to Office; LibreOffice Calc and Writer, to LibreOffice). Uninstalling any one removes the **whole bundle**, and the app warns you when the registered name differs from the item.
- Portable programs with no registered uninstaller: the app offers to open Windows "Installed apps".
- A broken shortcut has nothing to uninstall.

## Undo and history

- **Undo (Ctrl+Z)** reverts the last reversible action. **History…** lists the actions and lets you revert any of them.
- These can be undone: marking/unmarking a favorite, editing a description, moving to another category, hiding/showing, adding/removing a manual item, editing notes and tags, restoring a backup and sending a broken shortcut to the Recycle Bin (the app restores the copy it kept in `backup/atalhos`; if the folder requires permission, it asks for administrator confirmation).
- These can **not** be undone by the app: uninstalls and winget updates (they are recorded as "not reversible by the app").

## Top menus

The top buttons are now menus (the right-click menu and the footer buttons are unchanged):

- **File:** **Rescan** (`F5`; redoes the scan in about 1 min, the list appears right away and sizes are filled in as they are calculated), **Export…** (`Ctrl+E`; saves the displayed list, with search and filters, as CSV for Excel or as an HTML page with search), **Save configuration backup…**, **Restore backup…** and **Exit** (`Ctrl+Q`).
- **View:** **Switch light/dark theme** (at startup it follows the Windows theme), **Columns** (show or hide) and **Clear filters**.
- **Tools:** **Check updates**, **Programs summary…**, **Add program…**, **Undo** (`Ctrl+Z`) and **Action history…**.
- **🌐 Language:** chooses Português, English or Español (see "Language").
- **Help:** **Help** (`F1`: this window; **Go to index** returns to the top and **Open help file** opens the file), **Open project page** (GitHub) and **About App-Manager…** (version and license).

## Language

The **🌐 Language** menu (at the top) chooses the language of the interface, category names, the catalog's "what it does" descriptions and this Help: **Português, English and Español**. When you choose, the app reopens by itself.

- English is the default. The choice is kept in `user.json`.
- Not translated: program names, descriptions you wrote (Edit description…) and texts that come from the program itself (publisher, file description).
- The translated texts are in `lang/en.json` and `lang/es.json`; this Help exists as `help/pt.md`, `help/en.md` and `help/es.md`.

## Keyboard shortcuts

- `Ctrl+F`: go to search.
- `Down arrow` or `Enter` (in search): move to the list.
- `Esc` (in search): clear the search.
- `Enter` or double-click (in the list): open the program.
- `Ctrl+Z`: undo the last reversible action.
- `F5`: rescan.
- `Ctrl+E`: export the list.
- `Ctrl+Q`: close the app.
- `F1`: open the help.

## Portable .exe version

Besides the code (`App-Manager.bat`), there is `App-Manager.exe`, which **does not require Python**. Put it in a folder where you can write (for example `D:\Apps\App-Manager`): it creates `index.json`, `user.json`, `icons/` and `backup/` next to it. If the folder does not allow writing, it uses `%APPDATA%\App-Manager`. To update, just replace the `.exe`; your data stays. **Rescan** runs the `.exe` itself.

Windows (SmartScreen) or your antivirus may warn, because the `.exe` is new and has no digital signature. If you prefer, use the Python version.

## Files in the folder

- `index.json`: the index generated by the scan.
- `categories.json`: the default **catalog** (name words → category, subcategory and description) and fallback rules; it ships with the app.
- `categories.local.json` (optional, private): **your** catalog entries, the categories you moved, extra folders for `.bat` programs and `limpeza_dias`. Same format as `categories.json`; your entries win. `lang.local.en.json` / `lang.local.es.json` (optional) hold your own translations.
- `user.json`: your favorites, launch count and date, descriptions, notes, tags, hidden items, added items, chosen columns, language and the action history.
- `updates.json`: result of the last winget check. `usage.py`: reading of usage, startup and winget.
- `backup/atalhos/`: copies of the shortcuts sent to the Recycle Bin (used by Undo).
- `icons/`: icons extracted from the programs.
- `scan.py` (scan), `app.py` (the window), `usage.py`, `i18n.py`, `paths.py` and `version.py` (support), `lang/` (translations), `help/` (this Help, in 3 languages), `assets/` (logo and icon) and `App-Manager.bat` (to open it).

## Tips and limits

- Microsoft Store (UWP) programs and items without their own executable do not appear.
- The size is that of the whole install folder; programs in Windows folders show only the executable's size.
- Programs that are not in the catalog fall into "Other" or a fallback rule and may have no description: use right-click to fix it.
- To teach the catalog, edit `categories.local.json` (the `catalogo` list: `k` = parts of the name, `c` = category, `s` = subcategory, `d` = description; `=name` requires an exact name) and rescan. Descriptions you add are shown as written (in Portuguese, unless you write them in your language).
- Broken shortcuts are only a warning: check before sending them to the Recycle Bin.
