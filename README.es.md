<p align="center"><img src="assets/logo-256.png" alt="App-Manager" width="128"></p>

# App-Manager

[English](README.md) · [Português](README.pt.md) · **Español**

Catálogo de los programas instalados en **Windows**: qué hace cada uno, cuándo se usó, cuánto ocupa, categorías, y botones para abrir, actualizar o desinstalar. Python + Tkinter, sin dependencias externas, todo local. La interfaz viene en **inglés por defecto**, con **Português** y **Español** a un clic (menú 🌐 *Idioma*).

## Requisitos

| | |
|---|---|
| Sistema | **Windows 10 / 11** (usa el registro, el menú Inicio y `winget`; no funciona en Linux/macOS) |
| Versión `.exe` | Nada además de Windows |
| Versión Python | Python 3 con Tkinter y `python`/`pythonw` en el PATH (probado con Python 3.15 y Windows 11); solo biblioteca estándar |
| Opcional | [`winget`](https://learn.microsoft.com/windows/package-manager/winget/) para la columna y el menú de actualizaciones |

## Instalar y usar

**Opción A — `.exe` (sin Python):**
1. Descargue `App-Manager.exe` desde [Releases](https://github.com/thomasmeneghelli/App-Manager/releases).
2. Colóquelo en una carpeta donde pueda escribir (p. ej. `D:\Apps\App-Manager`) y haga doble clic. Crea sus datos al lado.
3. La primera vez escanea el PC (1–2 min). Windows SmartScreen puede avisar, porque el `.exe` no tiene firma digital.

**Opción B — Python:**
1. Instale [Python](https://www.python.org/downloads/) marcando **Add python.exe to PATH**.
2. Descargue este repositorio (**Code → Download ZIP**, o `git clone https://github.com/thomasmeneghelli/App-Manager.git`).
3. Doble clic en **`App-Manager.bat`**.

Para generar el `.exe` usted mismo: `build_exe.bat`. **F1** abre la Ayuda dentro de la aplicación.

## Qué hace

- Lee los accesos directos del menú Inicio y el registro de Windows; también encuentra programas que se abren con archivos `.bat`/`.cmd`.
- Categorías y subcategorías, descripción «para qué sirve», filtros por disco y tamaño, búsqueda (incluye sus notas y etiquetas).
- Columnas de **último uso**, veces usado y fecha de instalación (leídas de UserAssist de Windows).
- Listas predefinidas: favoritos, más usados, sugerencias de limpieza, inician con Windows, con actualización, versiones duplicadas.
- **Actualizar** con winget y **Desinstalar** con el desinstalador de Windows (pide la contraseña de UAC).
- **Deshacer**, historial, copia de seguridad de la configuración, resumen con gráficos y exportación CSV/HTML.
- Menús **Archivo, Ver, Herramientas, Idioma y Ayuda**, tema claro/oscuro y atajos (`F1`, `F5`, `Ctrl+F`, `Ctrl+E`, `Ctrl+Z`).

## Privacidad y seguridad

- Todo se ejecuta en su equipo; nada se envía a internet (solo `winget`, si pide actualizaciones).
- El escaneo y las lecturas del registro son **de solo lectura**.
- Actualizar y desinstalar **no se pueden deshacer** desde la aplicación; pide confirmación antes. Úselo bajo su responsabilidad.
- Sus datos (`user.json`, `index.json`, `updates.json`, `icons/`, `backup/`, `categories.local.json`) se crean localmente y git los ignora. El repositorio incluye solo un catálogo genérico de programas comunes.

## Personalizar

Añada sus programas y descripciones en `categories.local.json` (opcional, mismo formato que `categories.json`; sus entradas ganan) y reescanee. Traducciones en `lang/`. Ayuda completa: [English](help/en.md), [Português](help/pt.md), [Español](help/es.md).

## Licencia

[MIT](LICENSE)
