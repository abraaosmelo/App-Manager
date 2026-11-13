# App-Manager — Hilfe

## Inhaltsverzeichnis

- [Was es ist](#was-es-ist)
- [Navigation: Kategorien und Unterkategorien](#navigation-kategorien-und-unterkategorien)
- [Spalten: zuletzt verwendet, Verwendungen, installiert am](#spalten-zuletzt-verwendet-verwendungen-installiert-am)
- [Besondere Kategorien](#besondere-kategorien)
- [Aufräumvorschläge](#aufraumvorschlage)
- [Mit Windows starten](#mit-windows-starten)
- [Updates (winget)](#updates-winget)
- [Doppelte Versionen](#doppelte-versionen)
- [Notizen und Tags](#notizen-und-tags)
- [Übersicht](#ubersicht)
- [Konfigurationssicherung](#konfigurationssicherung)
- [Suchen und filtern (Laufwerk, Größe)](#suchen-und-filtern-laufwerk-groe)
- [Per .bat geöffnete Programme (portabel)](#per-bat-geoffnete-programme-portabel)
- [Einträge hinzufügen und ausblenden](#eintrage-hinzufugen-und-ausblenden)
- [Programme öffnen](#programme-offnen)
- [Rechtsklickmenü](#rechtsklickmenu)
- [Deinstallieren (fragt nach einem Passwort)](#deinstallieren-fragt-nach-einem-passwort)
- [Rückgängig und Verlauf](#ruckgangig-und-verlauf)
- [Obere Menüs](#obere-menus)
- [Sprache](#sprache)
- [Tastenkürzel](#tastenkurzel)
- [Portable .exe-Version](#portable-exe-version)
- [Dateien im Ordner](#dateien-im-ordner)
- [Tipps und Grenzen](#tipps-und-grenzen)

## Was es ist

Ein Verzeichnis der auf diesem PC installierten Programme, erstellt aus den **Startmenü-Verknüpfungen** (und aus einigen Programmen der Windows-Registrierung ohne Verknüpfung). Zu jedem zeigt es Name, Version, Installationsort, Größe, Laufwerk, Kategorie und **wozu es dient**.

Zum Öffnen: Doppelklick auf `App-Manager.bat` (oder `App-Manager.exe` in der portablen Version; siehe „Portable .exe-Version“).

Die App liest nur Informationen. Sie ändert nur dann etwas, wenn Sie es verlangen: deinstallieren, eine defekte Verknüpfung in den Papierkorb verschieben, in eine andere Kategorie verschieben usw.

## Navigation: Kategorien und Unterkategorien

- **Linker Bereich:** Kategorien mit der Anzahl der Programme. Klicken Sie auf den Pfeil, um die **Unterkategorien** zu öffnen (zum Beispiel Entwicklung › Editoren und IDEs).
- **Rechter Bereich:** Liste mit Symbol, Name, Version, Größe, Laufwerk, Kategorie › Unterkategorie und Speicherort. Klicken Sie auf einen Spaltentitel, um zu sortieren.
- **Fußzeile:** Details des ausgewählten Eintrags (Kategorie, Laufwerk, Version, Herausgeber, wie oft er von hier geöffnet wurde, Größe, Speicherort, ob es ein Deinstallationsprogramm gibt und wozu er dient).
- **Statusleiste** (oben rechts): Anzahl der angezeigten Einträge, „Größen werden berechnet…“, wie lange der letzte Scan her ist („gescannt vor 5 Min.“; ist er alt, verwenden Sie Neu scannen), neue und entfernte Einträge.

## Spalten: zuletzt verwendet, Verwendungen, installiert am

Die Tabelle hat diese Spalten (**Rechtsklick auf einen Spaltentitel**, um sie ein- oder auszublenden; es gibt „Standardspalten wiederherstellen“; die Tabelle scrollt waagerecht, wenn sie nicht passt): Name, Version, Update, Größe, Laufwerk, **Zuletzt verwendet**, **Verwendungen**, **Installiert am**, Startet mit Windows, Tags, Kategorie › Unterkategorie und Speicherort. Klicken Sie auf einen Titel, um zu sortieren.

- **Zuletzt verwendet und Verwendungen:** stammen aus der Windows-Registrierung (UserAssist), die festhält, wenn Sie ein Programm über den Explorer, das Startmenü, die Taskleiste oder den Desktop öffnen. Sie werden mit den Starts über dieses Verzeichnis zusammengeführt (die größere Zahl gewinnt, so wird nichts doppelt gezählt). Die Daten werden jedes Mal neu gelesen, wenn Sie zum Fenster zurückkehren. Die Spalte Zuletzt verwendet wird von selbst breiter, damit der längste Text hineinpasst.
- **„keine Daten“** bedeutet, dass Windows keinen Start notiert hat. Das **beweist nicht**, dass das Programm nie verwendet wurde: Windows erfasst keine Programme, die über die Kommandozeile, über `.bat`-Skripte, über Dienste oder über den Task-Manager geöffnet werden, und der Verlauf existiert erst, seit die Funktion aktiviert ist.
- **Installiert am:** das Installationsdatum aus der Windows-Registrierung, wenn vorhanden; sonst das Erstellungsdatum des Programmordners (das auch das Datum sein kann, an dem der Ordner kopiert wurde).

## Besondere Kategorien

- **Alle:** alles, was gefunden wurde.
- **★ Favoriten:** die Programme, die Sie markiert haben.
- **Meistverwendet:** die 15 am häufigsten gestarteten (Windows-Registrierung + dieses Verzeichnis).
- **Neu seit dem letzten Scan:** Programme, die nach dem vorherigen Scan hinzugekommen sind (markiert mit „(neu)“).
- **Ohne Startmenü-Verknüpfung:** installierte Programme ohne Verknüpfung, aber mit einer ausführbaren Datei, die sich öffnen lässt.
- **Aufräumvorschläge, Mit Windows starten, Mit Update und Doppelte Versionen:** siehe die folgenden Abschnitte.
- **Tags:** erscheint, sobald Sie Tags anlegen; jedes Tag wird zu einem Filter.
- **Ausgeblendet:** erscheint nur, wenn Sie einen Eintrag ausgeblendet haben (siehe „Einträge hinzufügen und ausblenden“).
- **Defekte Verknüpfungen:** Verknüpfungen, deren Programm nicht mehr existiert (wahrscheinlich deinstalliert). Die Unterkategorien zeigen, welche Art von Programm es war.

## Aufräumvorschläge

Listet die Programme auf, die **seit 180 Tagen oder länger nicht verwendet wurden oder für die keine Nutzungsdaten vorliegen**, vom größten zum kleinsten, und die Statusleiste zeigt, wie viel Platz das freigeben könnte (Ordner nur einmal gezählt). Nicht berücksichtigt werden: die Kategorie System, defekte Verknüpfungen und Ihre Favoriten.

Es ist nur ein Vorschlag. Da „keine Daten“ auch ein Programm sein kann, das Sie auf andere Weise nutzen, prüfen Sie jeden Eintrag, bevor Sie **Deinstallieren…** verwenden. Um den Zeitraum zu ändern, tragen Sie `"limpeza_dias": 365` in `categories.local.json` ein und öffnen Sie die App erneut.

## Mit Windows starten

Zeigt die Programme, die beim Hochfahren des PCs von selbst starten, gelesen aus den *Run*-Schlüsseln der Registrierung und dem Autostart-Ordner. Die Spalte **Startet mit Windows** zeigt **Ja** oder **Deaktiviert** (wenn Sie es im Task-Manager bereits ausgeschaltet haben); die Kategorie listet nur die aktiven auf. Die App zeigt sie nur an: Zum Ein- oder Ausschalten verwenden Sie die Registerkarte Autostart im Task-Manager. Die Zuordnung zwischen Eintrag und Programm erfolgt über den Pfad der ausführbaren Datei oder den Installationsordner, daher können mehrere Verknüpfungen desselben Programms erscheinen.

## Updates (winget)

- **Werkzeuge › Nach Updates suchen** fragt `winget` von Windows ab (etwa 15 s) und speichert das Ergebnis in `updates.json`.
- Einträge mit einer neuen Version erhalten die Spalte **Update** (→ Version), die Kategorie **Mit Update** und eine Detailzeile. Die Schaltfläche **Aktualisieren…** (oder Rechtsklick) führt `winget upgrade` in einem Konsolenfenster aus, mit Bestätigung; Windows fragt eventuell nach dem Administratorpasswort.
- Die App **kann ein Update nicht rückgängig machen**. Wenn sich das winget-Fenster schließt, fragt die App winget erneut ab (ohne Meldung) und entfernt bereits Aktualisiertes aus der Liste. Damit die Spalte Version die neue Version zeigt, klicken Sie auf Neu scannen.
- Es erscheinen nur Programme, die winget kennt und deren Name zum Eintrag passt; Windows-Komponenten, Treiber und Store-Apps bleiben außen vor.

## Doppelte Versionen

Die Kategorie **Doppelte Versionen** gruppiert ähnliche Einträge, zum Beispiel mehrere Pythons, zwei Visual Studios oder die Verknüpfungen „x86“ und „x64“. Das Detail zeigt die Gruppe und den gesamten Speicherplatz. Es hilft bei der Entscheidung, was deinstalliert werden soll; nicht jede Gruppe ist ein Problem (Verknüpfungen desselben Programms zählen ebenfalls dazu).

## Notizen und Tags

**Notizen und Tags…** (Schaltfläche in der Fußzeile oder Rechtsklick) öffnet ein Fenster, um Notizen (Lizenz, Download-Quelle, Projekt) und durch Kommas getrennte Tags zu schreiben. Tags erscheinen in der Kategorie **Tags** (ein Filter pro Tag) und in der Spalte Tags; die Suche berücksichtigt auch Notizen und Tags. Kann rückgängig gemacht werden.

## Übersicht

Das Menü **Werkzeuge › Programmübersicht…** öffnet einen Bildschirm mit: Anzahl der Programme und gesamtem Speicherplatz, Aufräumvorschlägen, wie viele mit Windows starten und ein Update haben, Gruppen doppelter Versionen, Speicherplatz nach Kategorie und nach Laufwerk, den 10 größten, den 10 meistverwendeten und den Installationen pro Jahr. Ausgeblendete Einträge und defekte Verknüpfungen werden nicht gezählt.

## Konfigurationssicherung

**Datei › Konfiguration sichern…** speichert alles, was Ihnen gehört, in einer `.json`-Datei: Favoriten, Anzahl und Datum der Verwendungen, bearbeitete Beschreibungen, Notizen, Tags, ausgeblendete Einträge, hinzugefügte Einträge, gewählte Spalten und verschobene Kategorien. **Datei › Sicherung wiederherstellen…** fragt, ob mit dem aktuellen Stand **zusammengeführt** oder ob er **ersetzt** werden soll; vorher bewahrt die App eine Kopie des aktuellen Stands in `backup/` auf, und Sie können es im Verlauf **rückgängig machen**. Nützlich, um Ihre Einrichtung auf einen anderen PC mitzunehmen oder nach einer Neuinstallation von Windows.

## Suchen und filtern (Laufwerk, Größe)

- **Suchen:** durchsucht Name, Beschreibung, Speicherort, Kategorie, Unterkategorie, Herausgeber, Notizen und Tags (auch die übersetzten Namen und Beschreibungen in der gewählten Sprache). Die Zahlen im linken Bereich passen sich an.
- **Laufwerk:** listet nur die Programme auf, die auf C:, D:, F: usw. installiert sind (die Buchstaben richten sich nach Ihrem PC).
- **Größe:** unter 100 MB, über 100 MB, 500 MB, 1 GB oder 5 GB. Programme, deren Größe noch „…“ ist (wird berechnet), bleiben bei diesen Filtern außen vor.
- **Filter zurücksetzen** stellt alles wieder normal dar. Suche und Filter wirken zusammen und gelten auch für den **Export**.

## Per .bat geöffnete Programme (portabel)

Manche Programme haben weder Installationsprogramm noch Verknüpfung: Man öffnet eine `run.bat` oder `start.bat` im Ordner (üblich bei portablen Programmen und KI-Werkzeugen). Der Scan sucht nach diesen `.bat`- und `.cmd`-Dateien und zeigt jeden **Ordner als einen Eintrag**, in der Kategorie **Programme ohne Installationsprogramm** (oder in einer anderen Kategorie, wenn der Katalog das Programm kennt).

- **Wo gesucht wird:** Downloads, Desktop, Dokumente und die Laufwerke außer dem Windows-Laufwerk (D:, F:…), bis zu 3 oder 4 Ordnerebenen tief. Um einen weiteren Ordner einzubeziehen, tragen Sie den Pfad in `categories.local.json` unter `"launchers": {"raizes_extra": ["E:\\Programme"]}` ein und scannen Sie neu.
- **Welche Dateien zählen:** Startnamen (`run`, `start`, `launch`, `iniciar`, `abrir`, `webui`…) oder die einzige `.bat` in einem Ordner. Ignoriert werden Installationsprogramme, Test- und Build-Skripte, interne Ordner (`venv`, `node_modules`, `bin`, `python_embeded`…) sowie Ordner von Programmen, die bereits über das Startmenü erscheinen.
- **Varianten:** Hat der Ordner mehrere Starter (`run.bat`, `run_anime.bat`…), öffnet der Eintrag den wichtigsten, und Rechtsklick > **Variante öffnen** listet die anderen auf.
- Die `.bat` läuft in ihrem eigenen Ordner, in einem Konsolenfenster. Solche Programme haben kein Deinstallationsprogramm: Zum Entfernen verwenden Sie **Ordner öffnen** und löschen den Ordner im Explorer.
- Es können Dinge erscheinen, die keine echten Programme sind (lose Skripte, Entwicklungswerkzeuge). Verwenden Sie in diesen Fällen **Ausblenden**.
- Der Scan dauert wegen dieser Suche auf den Laufwerken länger (etwa 1 Min. 30 s).

## Einträge hinzufügen und ausblenden

- **Hinzufügen…** (Schaltfläche in der Fußzeile): Wählen Sie eine `.exe`, `.bat`, `.cmd`, `.ps1`, `.py`, `.jar` oder `.lnk`, die der Scan nicht gefunden hat. Geben Sie den Namen ein und, wenn Sie möchten, wozu es dient. Der Eintrag landet unter *Programme ohne Installationsprogramm › Von mir hinzugefügt*. Zum Entfernen: Rechtsklick > **Selbst hinzugefügten Eintrag entfernen** (die Dateien werden nicht gelöscht).
- **In der Liste ausblenden** (Rechtsklick): blendet einen Eintrag in allen Ansichten und Zählungen aus. Ausgeblendete Einträge bleiben in der Kategorie **Ausgeblendet**, wo der Rechtsklick **Wieder in der Liste anzeigen** anbietet.
- Beides lässt sich rückgängig machen (Strg+Z oder Verlauf) und übersteht einen neuen Scan.

## Programme öffnen

- Doppelklick, `Enter` oder die Schaltfläche **Öffnen**: öffnet das Programm (über die Startmenü-Verknüpfung, wenn es eine gibt; `.bat`-Skripte laufen in ihrem eigenen Ordner).
- **Ordner öffnen:** öffnet den Installationsordner im Explorer.
- **★ Favorit:** markiert den ausgewählten Eintrag oder hebt die Markierung auf.

## Rechtsklickmenü

- **Öffnen**, **Ordner öffnen**, **Zu den Favoriten hinzufügen / Aus den Favoriten entfernen**, **Variante öffnen** (wenn der Ordner mehrere `.bat`-Dateien hat).
- **In der Liste ausblenden** / **Wieder in der Liste anzeigen** und **Selbst hinzugefügten Eintrag entfernen**: siehe „Einträge hinzufügen und ausblenden“.
- **Notizen und Tags…** und **Auf … aktualisieren (winget)**, wenn es eine neue Version gibt.
- **Beschreibung bearbeiten…:** ersetzt den Text „wozu es dient“ (gespeichert in `user.json`). Leer lassen, um zum Original zurückzukehren.
- **Deinstallieren…:** siehe den folgenden Abschnitt.
- **In Kategorie verschieben:** Wählen Sie Kategorie und Unterkategorie oder legen Sie neue an („Neue Unterkategorie…“, „Neue Kategorie…“). Das wird in `categories.local.json` gespeichert und gilt für künftige Scans.
- **Defekte Verknüpfung in den Papierkorb…:** erscheint nur bei defekten Verknüpfungen. Fragt nach Bestätigung, bewahrt eine Kopie der Verknüpfung auf und verschiebt sie in den Papierkorb (sie wird nicht endgültig gelöscht).

## Deinstallieren (fragt nach einem Passwort)

Die Schaltfläche **Deinstallieren…** (oder das Rechtsklickmenü) verwendet das Deinstallationsprogramm, das Windows selbst für das Programm registriert hat.

1. Die App zeigt den registrierten Namen und den Befehl, den sie ausführen wird, und fragt nach Bestätigung.
2. Sie fragt, ob Sie zuerst einen **Windows-Wiederherstellungspunkt erstellen** möchten. Damit können Sie über Windows zurückkehren (Systemwiederherstellung). Dafür muss der *Computerschutz* aktiviert sein; kann er nicht erstellt werden, wird nichts deinstalliert.
3. Windows fragt nach einer **Administratorbestätigung (Passwort)**, und das Deinstallationsprogramm läuft.
4. Danach bietet die App an, die Liste neu zu scannen.

> **Achtung:** Die App **kann eine Deinstallation nicht rückgängig machen**. Der einzige Weg zurück ist der Windows-Wiederherstellungspunkt oder eine Neuinstallation des Programms.

Worauf Sie achten sollten:

- Mehrere Verknüpfungen können zum selben Programm gehören (zum Beispiel gehören Word, Excel und Outlook zu Office; LibreOffice Calc und Writer zu LibreOffice). Die Deinstallation eines davon entfernt das **ganze Paket**, und die App warnt, wenn der registrierte Name vom Eintrag abweicht.
- Portable Programme ohne registriertes Deinstallationsprogramm: Die App bietet an, „Installierte Apps“ von Windows zu öffnen.
- Eine defekte Verknüpfung hat nichts zu deinstallieren.

## Rückgängig und Verlauf

- **Rückgängig (Strg+Z)** macht die letzte umkehrbare Aktion rückgängig. **Verlauf…** listet die Aktionen auf und lässt Sie jede davon rückgängig machen.
- Rückgängig machen lassen sich: Favoriten markieren/aufheben, eine Beschreibung bearbeiten, in eine andere Kategorie verschieben, ausblenden/anzeigen, einen manuellen Eintrag hinzufügen/entfernen, Notizen und Tags bearbeiten, eine Sicherung wiederherstellen und eine defekte Verknüpfung in den Papierkorb verschieben (die App stellt die in `backup/atalhos` aufbewahrte Kopie wieder her; erfordert der Ordner Berechtigungen, fragt sie nach einer Administratorbestätigung).
- **Nicht** rückgängig machen kann die App: Deinstallationen und winget-Updates (sie werden als „von der App nicht umkehrbar“ protokolliert).

## Obere Menüs

Die oberen Schaltflächen sind jetzt Menüs (das Rechtsklickmenü und die Schaltflächen in der Fußzeile bleiben unverändert):

- **Datei:** **Neu scannen** (`F5`; wiederholt den Scan in etwa 1 Min., die Liste erscheint sofort und die Größen werden ergänzt, sobald sie berechnet sind), **Exportieren…** (`Strg+E`; speichert die angezeigte Liste mit Suche und Filtern als CSV für Excel oder als HTML-Seite mit Suche), **Konfiguration sichern…**, **Sicherung wiederherstellen…** und **Beenden** (`Strg+Q`).
- **Ansicht:** **Helles/dunkles Design umschalten** (beim Start folgt es dem Windows-Design), **Spalten** (ein- oder ausblenden) und **Filter zurücksetzen**.
- **Werkzeuge:** **Nach Updates suchen**, **Programmübersicht…**, **Programm hinzufügen…**, **Rückgängig** (`Strg+Z`) und **Aktionsverlauf…**.
- **🌐 Sprache:** wählt Português, English, Español, Français oder Deutsch (siehe „Sprache“).
- **Hilfe:** **Hilfe** (`F1`: dieses Fenster; **Zum Inhaltsverzeichnis** springt nach oben und **Hilfedatei öffnen** öffnet die Datei), **Projektseite öffnen** (GitHub) und **Über App-Manager…** (Version und Lizenz).

## Sprache

Das Menü **🌐 Sprache** (oben) wählt die Sprache der Oberfläche, der Kategorienamen, der Beschreibungen „wozu es dient“ im Katalog und dieser Hilfe: **Português, English, Español, Français und Deutsch**. Nach der Auswahl öffnet sich die App von selbst neu.

- Englisch ist die Voreinstellung. Die Auswahl wird in `user.json` gespeichert.
- Nicht übersetzt werden: Programmnamen, selbst geschriebene Beschreibungen (Beschreibung bearbeiten…) und Texte, die vom Programm selbst stammen (Herausgeber, Dateibeschreibung).
- Die übersetzten Texte stehen in `lang/en.json`, `lang/es.json`, `lang/fr.json` und `lang/de.json`; diese Hilfe gibt es als `help/pt.md`, `help/en.md`, `help/es.md`, `help/fr.md` und `help/de.md`.

## Tastenkürzel

- `Strg+F`: zur Suche springen.
- `Pfeil nach unten` oder `Enter` (in der Suche): zur Liste wechseln.
- `Esc` (in der Suche): die Suche leeren.
- `Enter` oder Doppelklick (in der Liste): das Programm öffnen.
- `Strg+Z`: die letzte umkehrbare Aktion rückgängig machen.
- `F5`: neu scannen.
- `Strg+E`: die Liste exportieren.
- `Strg+Q`: die App schließen.
- `F1`: die Hilfe öffnen.

## Portable .exe-Version

Neben dem Code (`App-Manager.bat`) gibt es `App-Manager.exe`, das **kein Python benötigt**. Legen Sie es in einen Ordner mit Schreibrechten (zum Beispiel `D:\Apps\App-Manager`): Es erstellt daneben `index.json`, `user.json`, `icons/` und `backup/`. Erlaubt der Ordner kein Schreiben, verwendet es `%APPDATA%\App-Manager`. Zum Aktualisieren ersetzen Sie einfach die `.exe`; Ihre Daten bleiben erhalten. **Neu scannen** führt die `.exe` selbst aus.

Windows (SmartScreen) oder Ihr Virenschutz warnt eventuell, weil die `.exe` neu ist und keine digitale Signatur hat. Wenn Sie möchten, verwenden Sie die Python-Version.

## Dateien im Ordner

- `index.json`: das vom Scan erzeugte Verzeichnis.
- `categories.json`: der Standard-**Katalog** (Wörter im Namen → Kategorie, Unterkategorie und Beschreibung) und Ausweichregeln; wird mit der App geliefert.
- `categories.local.json` (optional, privat): **Ihre** Katalogeinträge, die von Ihnen verschobenen Kategorien, zusätzliche Ordner für `.bat`-Programme und `limpeza_dias`. Gleiches Format wie `categories.json`; Ihre Einträge haben Vorrang. `lang.local.<Sprache>.json` (optional, z. B. `lang.local.de.json`) enthalten Ihre eigenen Übersetzungen.
- `user.json`: Ihre Favoriten, Anzahl und Datum der Starts, Beschreibungen, Notizen, Tags, ausgeblendete Einträge, hinzugefügte Einträge, gewählte Spalten, Sprache und der Aktionsverlauf.
- `updates.json`: Ergebnis der letzten winget-Prüfung. `usage.py`: liest Nutzung, Autostart und winget.
- `backup/atalhos/`: Kopien der in den Papierkorb verschobenen Verknüpfungen (für Rückgängig).
- `icons/`: aus den Programmen extrahierte Symbole.
- `scan.py` (Scan), `app.py` (das Fenster), `usage.py`, `i18n.py`, `paths.py` und `version.py` (Hilfsmodule), `lang/` (Übersetzungen), `help/` (diese Hilfe, in 5 Sprachen), `assets/` (Logo und Symbol) und `App-Manager.bat` (zum Öffnen).

## Tipps und Grenzen

- Programme aus dem Microsoft Store (UWP) und Einträge ohne eigene ausführbare Datei erscheinen nicht.
- Die Größe ist die des gesamten Installationsordners; Programme in Windows-Ordnern zeigen nur die Größe der ausführbaren Datei.
- Programme, die nicht im Katalog stehen, landen unter „Sonstiges“ oder in einer Ausweichregel und haben eventuell keine Beschreibung: Korrigieren Sie das per Rechtsklick.
- Um dem Katalog etwas beizubringen, bearbeiten Sie `categories.local.json` (die Liste `catalogo`: `k` = Teile des Namens, `c` = Kategorie, `s` = Unterkategorie, `d` = Beschreibung; `=name` verlangt einen exakten Namen) und scannen Sie neu. Selbst hinzugefügte Beschreibungen werden so angezeigt, wie sie geschrieben wurden (auf Portugiesisch, sofern Sie sie nicht in Ihrer Sprache schreiben).
- Defekte Verknüpfungen sind nur ein Hinweis: Prüfen Sie sie, bevor Sie sie in den Papierkorb verschieben.
