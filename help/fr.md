# App-Manager — Aide

## Index

- [Présentation](#presentation)
- [Navigation : catégories et sous-catégories](#navigation-categories-et-sous-categories)
- [Colonnes : dernière utilisation, utilisations, installé le](#colonnes-derniere-utilisation-utilisations-installe-le)
- [Catégories spéciales](#categories-speciales)
- [Suggestions de nettoyage](#suggestions-de-nettoyage)
- [Démarrent avec Windows](#demarrent-avec-windows)
- [Mises à jour (winget)](#mises-a-jour-winget)
- [Versions en double](#versions-en-double)
- [Notes et étiquettes](#notes-et-etiquettes)
- [Résumé](#resume)
- [Sauvegarde de la configuration](#sauvegarde-de-la-configuration)
- [Recherche et filtres (disque, taille)](#recherche-et-filtres-disque-taille)
- [Programmes ouverts par .bat (portables)](#programmes-ouverts-par-bat-portables)
- [Ajouter et masquer des éléments](#ajouter-et-masquer-des-elements)
- [Ouvrir des programmes](#ouvrir-des-programmes)
- [Menu du clic droit](#menu-du-clic-droit)
- [Désinstaller (demande un mot de passe)](#desinstaller-demande-un-mot-de-passe)
- [Annuler et historique](#annuler-et-historique)
- [Menus du haut](#menus-du-haut)
- [Langue](#langue)
- [Raccourcis clavier](#raccourcis-clavier)
- [Version .exe portable](#version-exe-portable)
- [Fichiers du dossier](#fichiers-du-dossier)
- [Conseils et limites](#conseils-et-limites)

## Présentation

Un index des programmes installés sur ce PC, construit à partir des **raccourcis du menu Démarrer** (et de quelques programmes du registre Windows qui n'ont pas de raccourci). Pour chacun, il affiche le nom, la version, l'emplacement d'installation, la taille, le disque, la catégorie et **à quoi il sert**.

Pour l'ouvrir : double-cliquez sur `App-Manager.bat` (ou `App-Manager.exe` dans la version portable ; voir « Version .exe portable »).

L'application ne fait que lire des informations. Elle ne modifie quelque chose que si vous le demandez : désinstaller, envoyer un raccourci cassé à la Corbeille, déplacer vers une autre catégorie, etc.

## Navigation : catégories et sous-catégories

- **Volet de gauche :** les catégories avec le nombre de programmes. Cliquez sur la flèche pour ouvrir les **sous-catégories** (par exemple, Développement › Éditeurs et IDE).
- **Volet de droite :** la liste avec icône, nom, version, taille, disque, catégorie › sous-catégorie et emplacement. Cliquez sur le titre d'une colonne pour trier.
- **Bas de la fenêtre :** les détails de l'élément sélectionné (catégorie, disque, version, éditeur, nombre d'ouvertures depuis ici, taille, emplacement, présence d'un programme de désinstallation et à quoi il sert).
- **Barre d'état** (en haut à droite) : total affiché, « calcul des tailles… », ancienneté de la dernière analyse (« analysé il y a 5 min » ; si elle est ancienne, utilisez Analyser à nouveau), nouveaux et supprimés.

## Colonnes : dernière utilisation, utilisations, installé le

Le tableau contient ces colonnes (**clic droit sur le titre d'une colonne** pour l'afficher ou la masquer ; il existe « Rétablir les colonnes par défaut » ; le tableau défile horizontalement s'il ne tient pas) : Nom, Version, Mise à jour, Taille, Disque, **Dernière utilisation**, **Utilisations**, **Installé le**, Démarre avec Windows, Étiquettes, Catégorie › Sous-catégorie et Emplacement. Cliquez sur un titre pour trier.

- **Dernière utilisation et Utilisations :** proviennent du registre Windows (UserAssist), qui note quand vous ouvrez un programme depuis l'Explorateur, le menu Démarrer, la barre des tâches ou le bureau. Elles s'ajoutent aux lancements faits depuis cet index (le plus grand nombre l'emporte, pour ne rien compter deux fois). Les données sont relues chaque fois que vous revenez à la fenêtre. La colonne Dernière utilisation s'élargit d'elle-même pour afficher le texte le plus long.
- **« aucun enregistrement »** signifie que Windows n'a noté aucun lancement. Cela **ne prouve pas** que le programme n'a jamais été utilisé : Windows n'enregistre pas les programmes ouverts depuis la ligne de commande, des scripts `.bat`, des services ou le Gestionnaire des tâches, et l'historique n'existe que depuis l'activation de la fonction.
- **Installé le :** la date d'installation du registre Windows quand elle existe ; sinon la date de création du dossier du programme (qui peut être la date à laquelle le dossier a été copié).

## Catégories spéciales

- **Tous :** tout ce qui a été trouvé.
- **★ Favoris :** les programmes que vous avez marqués.
- **Les plus utilisés :** les 15 plus lancés (registre Windows + cet index).
- **Nouveaux depuis la dernière analyse :** les programmes apparus après l'analyse précédente (marqués « (nouveau) »).
- **Sans raccourci dans le menu Démarrer :** programmes installés sans raccourci mais avec un exécutable qui peut être ouvert.
- **Suggestions de nettoyage, Démarrent avec Windows, Avec mise à jour et Versions en double :** voir les sections ci-dessous.
- **Étiquettes :** apparaît quand vous créez des étiquettes ; chaque étiquette devient un filtre.
- **Masqués :** n'apparaît que si vous avez masqué un élément (voir « Ajouter et masquer des éléments »).
- **Raccourcis cassés :** raccourcis dont le programme n'existe plus (probablement désinstallé). Leurs sous-catégories indiquent le type de programme.

## Suggestions de nettoyage

Liste les programmes **inutilisés depuis 180 jours ou plus, ou sans enregistrement d'utilisation**, du plus grand au plus petit, et la barre d'état indique l'espace qui pourrait être libéré (dossiers comptés une seule fois). Sont exclus : la catégorie Système, les raccourcis cassés et vos favoris.

Ce n'est qu'une suggestion. Comme « aucun enregistrement » peut être un programme que vous utilisez autrement, vérifiez chaque élément avant d'utiliser **Désinstaller…**. Pour changer la période, mettez `"limpeza_dias": 365` dans `categories.local.json` et rouvrez l'application.

## Démarrent avec Windows

Affiche les programmes qui démarrent tout seuls au lancement du PC, lus dans les clés *Run* du registre et dans le dossier Démarrage. La colonne **Démarre avec Windows** indique **Oui** ou **Désactivé** (quand vous l'avez déjà désactivé dans le Gestionnaire des tâches) ; la catégorie ne liste que les actifs. L'application ne fait que les afficher : pour les activer ou les désactiver, utilisez l'onglet Démarrage du Gestionnaire des tâches. Le lien entre l'entrée et le programme se fait par le chemin de l'exécutable ou le dossier d'installation, il peut donc lister plusieurs raccourcis du même programme.

## Mises à jour (winget)

- **Outils › Rechercher des mises à jour** interroge `winget` de Windows (environ 15 s) et enregistre le résultat dans `updates.json`.
- Les éléments ayant une nouvelle version reçoivent la colonne **Mise à jour** (→ version), la catégorie **Avec mise à jour** et une ligne de détail. Le bouton **Mettre à jour…** (ou le clic droit) exécute `winget upgrade` dans une fenêtre de console, avec confirmation ; Windows peut demander le mot de passe administrateur.
- L'application **ne peut pas annuler** une mise à jour. Quand la fenêtre de winget se ferme, l'application interroge à nouveau winget (sans message) et retire de la liste ce qui a déjà été mis à jour. Pour que la colonne Version affiche la nouvelle version, cliquez sur Analyser à nouveau.
- N'apparaissent que les programmes connus de winget et dont le nom correspond à l'élément ; les composants de Windows, les pilotes et les applications du Store sont exclus.

## Versions en double

La catégorie **Versions en double** regroupe des éléments semblables, par exemple plusieurs Python, deux Visual Studio ou les raccourcis « x86 » et « x64 ». Le détail montre le groupe et l'espace total. Cela vous aide à décider quoi désinstaller ; tout groupe n'est pas un problème (les raccourcis d'un même programme sont aussi inclus).

## Notes et étiquettes

**Notes et étiquettes…** (bouton du bas ou clic droit) ouvre une fenêtre pour écrire des notes (licence, où vous l'avez téléchargé, projet) et des étiquettes séparées par des virgules. Les étiquettes apparaissent dans la catégorie **Étiquettes** (un filtre par étiquette) et dans la colonne Étiquettes ; la recherche porte aussi sur les notes et les étiquettes. C'est annulable.

## Résumé

Le menu **Outils › Résumé des programmes…** ouvre un écran avec : le nombre de programmes et l'espace total, les suggestions de nettoyage, combien démarrent avec Windows et ont une mise à jour, les groupes en double, l'espace par catégorie et par disque, les 10 plus volumineux, les 10 plus utilisés et les installations par année. Les éléments masqués et les raccourcis cassés ne sont pas comptés.

## Sauvegarde de la configuration

**Fichier › Enregistrer une sauvegarde de la configuration…** enregistre dans un fichier `.json` tout ce qui vous appartient : favoris, nombre et date d'utilisations, descriptions modifiées, notes, étiquettes, éléments masqués, éléments ajoutés, colonnes choisies et catégories déplacées. **Fichier › Restaurer une sauvegarde…** demande s'il faut **fusionner** avec l'existant ou **remplacer** ; avant cela, l'application garde une copie de l'état actuel dans `backup/`, et vous pouvez **annuler** depuis l'Historique. Pratique pour emporter votre configuration sur un autre PC ou après une réinstallation de Windows.

## Recherche et filtres (disque, taille)

- **Recherche :** cherche dans le nom, la description, l'emplacement, la catégorie, la sous-catégorie, l'éditeur, les notes et les étiquettes (aussi dans les noms et descriptions traduits, dans la langue choisie). Les compteurs du volet de gauche s'ajustent.
- **Disque :** ne liste que les programmes installés sur C:, D:, F: etc. (les lettres dépendent de votre PC).
- **Taille :** moins de 100 MB, plus de 100 MB, 500 MB, 1 GB ou 5 GB. Les programmes dont la taille est encore « … » (en cours de calcul) sont exclus de ces filtres.
- **Effacer les filtres** remet tout à la normale. Recherche et filtres se combinent et s'appliquent aussi à l'**export**.

## Programmes ouverts par .bat (portables)

Certains programmes n'ont ni installateur ni raccourci : on ouvre un `run.bat` ou `start.bat` dans leur dossier (courant pour les programmes portables et les outils d'IA). L'analyse cherche ces fichiers `.bat` et `.cmd` et affiche chaque **dossier comme un seul élément**, dans la catégorie **Programmes sans installateur** (ou dans une autre catégorie, si le catalogue connaît le programme).

- **Où elle cherche :** Téléchargements, Bureau, Documents et les disques autres que celui de Windows (D:, F:…), jusqu'à 3 ou 4 niveaux de dossiers. Pour inclure un autre dossier, mettez le chemin dans `categories.local.json`, sous `"launchers": {"raizes_extra": ["E:\\Programmes"]}`, et analysez à nouveau.
- **Quels fichiers comptent :** les noms de démarrage (`run`, `start`, `launch`, `iniciar`, `abrir`, `webui`…), ou le seul `.bat` d'un dossier. Elle ignore les installateurs, les scripts de test et de compilation, et les dossiers internes (`venv`, `node_modules`, `bin`, `python_embeded`…), ainsi que les dossiers de programmes qui apparaissent déjà via le menu Démarrer.
- **Variantes :** si le dossier contient plusieurs lanceurs (`run.bat`, `run_anime.bat`…), l'élément ouvre le principal et le clic droit > **Ouvrir une variante** liste les autres.
- Le `.bat` s'exécute dans son propre dossier, dans une fenêtre de console. Ces programmes n'ont pas de programme de désinstallation : pour en supprimer un, utilisez **Ouvrir le dossier** et effacez le dossier dans l'Explorateur.
- Des choses qui ne sont pas vraiment des programmes peuvent apparaître (scripts isolés, outils de développement). Utilisez **Masquer** dans ces cas.
- L'analyse prend plus de temps (environ 1 min 30 s) à cause de cette recherche sur les disques.

## Ajouter et masquer des éléments

- **Ajouter…** (bouton du bas) : choisissez un `.exe`, `.bat`, `.cmd`, `.ps1`, `.py`, `.jar` ou `.lnk` que l'analyse n'a pas trouvé. Saisissez le nom et, si vous voulez, à quoi il sert. Il va dans *Programmes sans installateur › Ajoutés par moi*. Pour le retirer : clic droit > **Retirer un élément que j'ai ajouté** (les fichiers ne sont pas supprimés).
- **Masquer de la liste** (clic droit) : masque un élément de tous les écrans et compteurs. Les éléments masqués restent dans la catégorie **Masqués**, où le clic droit propose **Afficher à nouveau dans la liste**.
- Les deux sont annulables (Ctrl+Z ou Historique) et survivent à une nouvelle analyse.

## Ouvrir des programmes

- Double-clic, `Entrée` ou le bouton **Ouvrir** : ouvre le programme (via le raccourci du menu Démarrer, s'il existe ; les scripts `.bat` s'exécutent dans leur propre dossier).
- **Ouvrir le dossier :** ouvre le dossier d'installation dans l'Explorateur.
- **★ Favori :** marque ou démarque l'élément sélectionné.

## Menu du clic droit

- **Ouvrir**, **Ouvrir le dossier**, **Ajouter aux / Retirer des favoris**, **Ouvrir une variante** (quand le dossier contient plusieurs fichiers `.bat`).
- **Masquer de la liste** / **Afficher à nouveau dans la liste** et **Retirer un élément que j'ai ajouté** : voir « Ajouter et masquer des éléments ».
- **Notes et étiquettes…**, et **Mettre à jour vers… (winget)** quand il existe une nouvelle version.
- **Modifier la description… :** remplace le texte « à quoi ça sert » (gardé dans `user.json`). Laissez-le vide pour revenir à l'original.
- **Désinstaller… :** voir la section ci-dessous.
- **Déplacer vers la catégorie :** choisissez la catégorie et la sous-catégorie, ou créez-en de nouvelles (« Nouvelle sous-catégorie… », « Nouvelle catégorie… »). C'est enregistré dans `categories.local.json` et s'applique aux analyses suivantes.
- **Envoyer le raccourci cassé à la Corbeille… :** n'apparaît que sur les raccourcis cassés. Demande une confirmation, garde une copie du raccourci et l'envoie à la Corbeille (il n'est pas supprimé définitivement).

## Désinstaller (demande un mot de passe)

Le bouton **Désinstaller…** (ou le menu du clic droit) utilise le programme de désinstallation que Windows a lui-même enregistré pour le programme.

1. L'application affiche le nom enregistré et la commande qu'elle va exécuter, et demande une confirmation.
2. Elle demande si vous voulez d'abord **créer un point de restauration Windows**. Avec lui, vous pouvez revenir en arrière via Windows (Restauration du système). Il faut que la *Protection du système* soit activée ; s'il ne peut pas être créé, rien n'est désinstallé.
3. Windows demande une **confirmation administrateur (mot de passe)**, et le programme de désinstallation s'exécute.
4. À la fin, l'application propose d'analyser à nouveau la liste.

> **Attention :** l'application **ne peut pas annuler** une désinstallation. Le seul retour possible est le point de restauration Windows ou la réinstallation du programme.

Points d'attention :

- Plusieurs raccourcis peuvent appartenir au même programme (par exemple, Word, Excel et Outlook appartiennent à Office ; LibreOffice Calc et Writer, à LibreOffice). En désinstaller un supprime **l'ensemble**, et l'application vous prévient quand le nom enregistré diffère de l'élément.
- Programmes portables sans programme de désinstallation enregistré : l'application propose d'ouvrir « Applications installées » de Windows.
- Un raccourci cassé n'a rien à désinstaller.

## Annuler et historique

- **Annuler (Ctrl+Z)** annule la dernière action réversible. **Historique…** liste les actions et permet d'annuler n'importe laquelle.
- Sont annulables : marquer/démarquer un favori, modifier une description, déplacer vers une autre catégorie, masquer/afficher, ajouter/retirer un élément manuel, modifier notes et étiquettes, restaurer une sauvegarde et envoyer un raccourci cassé à la Corbeille (l'application restaure la copie gardée dans `backup/atalhos` ; si le dossier exige une autorisation, elle demande une confirmation administrateur).
- **Ne sont pas** annulables par l'application : les désinstallations et les mises à jour winget (elles sont notées « non réversible par l'application »).

## Menus du haut

Les boutons du haut sont désormais des menus (le menu du clic droit et les boutons du bas n'ont pas changé) :

- **Fichier :** **Analyser à nouveau** (`F5` ; refait l'analyse en environ 1 min, la liste apparaît tout de suite et les tailles se remplissent au fur et à mesure), **Exporter…** (`Ctrl+E` ; enregistre la liste affichée, avec recherche et filtres, en CSV pour Excel ou en page HTML avec recherche), **Enregistrer une sauvegarde de la configuration…**, **Restaurer une sauvegarde…** et **Quitter** (`Ctrl+Q`).
- **Affichage :** **Basculer thème clair/sombre** (au démarrage, il suit le thème de Windows), **Colonnes** (afficher ou masquer) et **Effacer les filtres**.
- **Outils :** **Rechercher des mises à jour**, **Résumé des programmes…**, **Ajouter un programme…**, **Annuler** (`Ctrl+Z`) et **Historique des actions…**.
- **🌐 Langue :** choisit Português, English, Español, Français ou Deutsch (voir « Langue »).
- **Aide :** **Aide** (`F1` : cette fenêtre ; **Aller à l'index** revient en haut et **Ouvrir le fichier d'aide** ouvre le fichier), **Ouvrir la page du projet** (GitHub) et **À propos de App-Manager…** (version et licence).

## Langue

Le menu **🌐 Langue** (en haut) choisit la langue de l'interface, des noms de catégories, des descriptions « à quoi ça sert » du catalogue et de cette Aide : **Português, English, Español, Français et Deutsch**. Quand vous choisissez, l'application se rouvre d'elle-même.

- L'anglais est la langue par défaut. Le choix est gardé dans `user.json`.
- Ne sont pas traduits : les noms des programmes, les descriptions que vous avez écrites (Modifier la description…) et les textes qui viennent du programme lui-même (éditeur, description du fichier).
- Les textes traduits sont dans `lang/en.json`, `lang/es.json`, `lang/fr.json` et `lang/de.json` ; cette Aide existe en `help/pt.md`, `help/en.md`, `help/es.md`, `help/fr.md` et `help/de.md`.

## Raccourcis clavier

- `Ctrl+F` : aller à la recherche.
- `Flèche bas` ou `Entrée` (dans la recherche) : passer à la liste.
- `Échap` (dans la recherche) : effacer la recherche.
- `Entrée` ou double-clic (dans la liste) : ouvrir le programme.
- `Ctrl+Z` : annuler la dernière action réversible.
- `F5` : analyser à nouveau.
- `Ctrl+E` : exporter la liste.
- `Ctrl+Q` : fermer l'application.
- `F1` : ouvrir l'aide.

## Version .exe portable

En plus du code (`App-Manager.bat`), il existe `App-Manager.exe`, qui **ne nécessite pas Python**. Placez-le dans un dossier où vous pouvez écrire (par exemple `D:\Apps\App-Manager`) : il crée à côté `index.json`, `user.json`, `icons/` et `backup/`. Si le dossier ne permet pas l'écriture, il utilise `%APPDATA%\App-Manager`. Pour le mettre à jour, remplacez seulement le `.exe` ; vos données restent. **Analyser à nouveau** exécute le `.exe` lui-même.

Windows (SmartScreen) ou votre antivirus peut afficher un avertissement, car le `.exe` est nouveau et n'a pas de signature numérique. Si vous préférez, utilisez la version Python.

## Fichiers du dossier

- `index.json` : l'index généré par l'analyse.
- `categories.json` : le **catalogue** par défaut (mots du nom → catégorie, sous-catégorie et description) et les règles de repli ; il est fourni avec l'application.
- `categories.local.json` (facultatif, privé) : **vos** entrées de catalogue, les catégories que vous avez déplacées, les dossiers supplémentaires pour les programmes `.bat` et `limpeza_dias`. Même format que `categories.json` ; vos entrées l'emportent. `lang.local.<langue>.json` (facultatif, par exemple `lang.local.fr.json`) contient vos propres traductions.
- `user.json` : vos favoris, le nombre et la date des lancements, les descriptions, notes, étiquettes, éléments masqués, éléments ajoutés, colonnes choisies, la langue et l'historique des actions.
- `updates.json` : résultat de la dernière recherche winget. `usage.py` : lecture de l'utilisation, du démarrage et de winget.
- `backup/atalhos/` : copies des raccourcis envoyés à la Corbeille (utilisées par Annuler).
- `icons/` : icônes extraites des programmes.
- `scan.py` (analyse), `app.py` (la fenêtre), `usage.py`, `i18n.py`, `paths.py` et `version.py` (support), `lang/` (traductions), `help/` (cette Aide, en 5 langues), `assets/` (logo et icône) et `App-Manager.bat` (pour l'ouvrir).

## Conseils et limites

- Les programmes du Microsoft Store (UWP) et les éléments sans exécutable propre n'apparaissent pas.
- La taille est celle de tout le dossier d'installation ; les programmes situés dans les dossiers de Windows n'affichent que la taille de l'exécutable.
- Les programmes absents du catalogue tombent dans « Autres » ou dans une règle de repli et peuvent ne pas avoir de description : utilisez le clic droit pour corriger.
- Pour enrichir le catalogue, modifiez `categories.local.json` (la liste `catalogo` : `k` = parties du nom, `c` = catégorie, `s` = sous-catégorie, `d` = description ; `=nom` exige un nom exact) et analysez à nouveau. Les descriptions que vous ajoutez s'affichent telles qu'écrites (en portugais, sauf si vous les écrivez dans votre langue).
- Les raccourcis cassés ne sont qu'un avertissement : vérifiez avant de les envoyer à la Corbeille.
