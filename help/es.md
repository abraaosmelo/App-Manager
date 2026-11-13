# App-Manager — Ayuda

## Índice

- [Qué es](#que-es)
- [Navegar: categorías y subcategorías](#navegar-categorias-y-subcategorias)
- [Columnas: último uso, veces usado, instalado el](#columnas-ultimo-uso-veces-usado-instalado-el)
- [Categorías especiales](#categorias-especiales)
- [Sugerencias de limpieza](#sugerencias-de-limpieza)
- [Inician con Windows](#inician-con-windows)
- [Actualizaciones (winget)](#actualizaciones-winget)
- [Versiones duplicadas](#versiones-duplicadas)
- [Notas y etiquetas](#notas-y-etiquetas)
- [Resumen](#resumen)
- [Copia de seguridad de la configuración](#copia-de-seguridad-de-la-configuracion)
- [Buscar y filtrar (disco, tamaño)](#buscar-y-filtrar-disco-tamano)
- [Programas que se abren con .bat (portátiles)](#programas-que-se-abren-con-bat-portatiles)
- [Añadir y ocultar elementos](#anadir-y-ocultar-elementos)
- [Abrir programas](#abrir-programas)
- [Menú del clic derecho](#menu-del-clic-derecho)
- [Desinstalar (pide contraseña)](#desinstalar-pide-contrasena)
- [Deshacer e historial](#deshacer-e-historial)
- [Menús superiores](#menus-superiores)
- [Idioma](#idioma)
- [Atajos de teclado](#atajos-de-teclado)
- [Versión .exe portátil](#version-exe-portatil)
- [Archivos de la carpeta](#archivos-de-la-carpeta)
- [Consejos y límites](#consejos-y-limites)

## Qué es

Un índice de los programas instalados en este PC, construido a partir de los **accesos directos del menú Inicio** (y de algunos programas del registro de Windows que no tienen acceso directo). De cada uno muestra nombre, versión, ubicación de instalación, tamaño, disco, categoría y **para qué sirve**.

Para abrirlo: doble clic en `App-Manager.bat` (o en `App-Manager.exe`, en la versión portátil; vea «Versión .exe portátil»).

La aplicación solo lee información. Cambia algo únicamente cuando usted lo pide: desinstalar, enviar un acceso directo roto a la Papelera, mover de categoría, etc.

## Navegar: categorías y subcategorías

- **Panel izquierdo:** categorías con el número de programas. Haga clic en la flecha para abrir las **subcategorías** (por ejemplo, Desarrollo › Editores e IDE).
- **Panel derecho:** lista con icono, nombre, versión, tamaño, disco, categoría › subcategoría y ubicación. Haga clic en el título de una columna para ordenar.
- **Pie:** detalles del elemento seleccionado (categoría, disco, versión, fabricante, cuántas veces se abrió desde aquí, tamaño, ubicación, si hay desinstalador y para qué sirve).
- **Barra de estado** (arriba a la derecha): total mostrado, «calculando tamaños…», hace cuánto se hizo el último escaneo («escaneado hace 5 min»; si es antiguo, use Reescanear), nuevos y eliminados.

## Columnas: último uso, veces usado, instalado el

La tabla tiene estas columnas (haga **clic derecho en el título** de cualquier columna para mostrarla u ocultarla; existe «Restaurar columnas predeterminadas»; la tabla tiene desplazamiento horizontal si no cabe): Nombre, Versión, Actualización, Tamaño, Disco, **Último uso**, **Veces usado**, **Instalado el**, Inicia con Windows, Etiquetas, Categoría › Subcategoría y Ubicación. Haga clic en el título para ordenar.

- **Último uso y Veces usado:** vienen del registro de Windows (UserAssist), que anota cuándo abre un programa desde el Explorador, el menú Inicio, la barra de tareas o el escritorio. Se suman a las aperturas hechas desde este índice (vale el número mayor, para no contar dos veces). Los datos se leen de nuevo cada vez que vuelve a la ventana.
- **«sin registro»** significa que Windows no anotó ninguna apertura. Esto **no demuestra** que el programa nunca se haya usado: Windows no registra programas abiertos por línea de comandos, por scripts `.bat`, por servicios o desde el Administrador de tareas, y el historial solo existe desde que se activó la función.
- **Instalado el:** fecha de instalación del registro de Windows cuando existe; si no, la fecha de creación de la carpeta del programa (puede ser la fecha en que se copió la carpeta).

## Categorías especiales

- **Todos:** todo lo que se encontró.
- **★ Favoritos:** los programas que usted marcó.
- **Más usados:** los 15 con más aperturas (registro de Windows + este índice).
- **Nuevos desde el último escaneo:** programas que aparecieron después del escaneo anterior (marcados con «(nuevo)»).
- **Sin acceso directo en el menú Inicio:** programas instalados que no tienen acceso directo, pero sí un ejecutable que se puede abrir.
- **Sugerencias de limpieza, Inician con Windows, Con actualización y Versiones duplicadas:** vea las secciones siguientes.
- **Etiquetas:** aparece cuando crea etiquetas; cada etiqueta se convierte en un filtro.
- **Ocultos:** aparece solo cuando ha ocultado algún elemento (vea «Añadir y ocultar elementos»).
- **Accesos directos rotos:** accesos directos cuyo programa ya no existe (probablemente desinstalado). Sus subcategorías muestran el tipo de programa que era.

## Sugerencias de limpieza

Lista los programas **sin uso hace 180 días o más, o sin registro de uso**, del mayor al menor, y la barra de estado muestra cuánto espacio podría liberar (carpetas contadas una vez). Quedan fuera: la categoría Sistema, los accesos directos rotos y sus favoritos.

Es solo una sugerencia. Como «sin registro» puede ser un programa que usa por otros caminos, revise cada elemento antes de usar **Desinstalar…**. Para cambiar el plazo, ponga `"limpeza_dias": 365` en `categories.local.json` y vuelva a abrir la aplicación.

## Inician con Windows

Muestra los programas que se abren solos al encender el PC, leídos de las claves *Run* del registro y de la carpeta Inicio. La columna **Inicia con Windows** indica **Sí** o **Desactivado** (cuando ya lo desactivó en el Administrador de tareas); la categoría lista solo los activos. La aplicación solo lo muestra: para activarlos o desactivarlos, use la pestaña Inicio del Administrador de tareas. El vínculo entre la entrada y el programa es por la ruta del ejecutable o por la carpeta de instalación, así que puede listar varios accesos directos del mismo programa.

## Actualizaciones (winget)

- **Herramientas › Buscar actualizaciones** consulta el `winget` de Windows (unos 15 s) y guarda el resultado en `updates.json`.
- Los elementos con versión nueva reciben la columna **Actualización** (→ versión), la categoría **Con actualización** y una línea de detalle. El botón **Actualizar…** (o clic derecho) ejecuta `winget upgrade` en una ventana de consola, con confirmación; Windows puede pedir contraseña de administrador.
- La aplicación **no puede deshacer** una actualización. Cuando se cierra la ventana de winget, la aplicación consulta winget de nuevo (sin mensaje) y quita de la lista lo que ya se actualizó. Para que la columna Versión muestre la versión nueva, haga clic en Reescanear.
- Solo aparecen programas que winget conoce y que coinciden con el nombre del elemento; los componentes de Windows, controladores y apps de la Tienda quedan fuera.

## Versiones duplicadas

La categoría **Versiones duplicadas** agrupa elementos parecidos, por ejemplo varios Python, dos Visual Studio o los accesos directos «x86» y «x64». El detalle muestra el grupo y el espacio total. Sirve para decidir qué desinstalar; no todo grupo es un problema (los accesos directos del mismo programa también entran).

## Notas y etiquetas

**Notas y etiquetas…** (botón del pie o clic derecho) abre una ventana para escribir anotaciones (licencia, dónde lo descargó, proyecto) y etiquetas separadas por comas. Las etiquetas aparecen en la categoría **Etiquetas** (un filtro por etiqueta) y en la columna Etiquetas; la búsqueda también mira notas y etiquetas. Se puede deshacer.

## Resumen

El menú **Herramientas › Resumen de los programas…** abre una pantalla con: número de programas y espacio total, sugerencias de limpieza, cuántos inician con Windows y tienen actualización, grupos duplicados, espacio por categoría y por disco, los 10 mayores, los 10 más usados e instalaciones por año. Los elementos ocultos y los accesos directos rotos no cuentan.

## Copia de seguridad de la configuración

**Archivo › Guardar copia de la configuración…** guarda en un archivo `.json` todo lo que es suyo: favoritos, recuento y fecha de uso, descripciones editadas, notas, etiquetas, elementos ocultos, elementos añadidos, columnas elegidas y categorías movidas. **Archivo › Restaurar copia…** pregunta si debe **combinar** con lo que existe o **reemplazar**; antes de eso la aplicación guarda una copia del estado actual en `backup/` y se puede **deshacer** desde el Historial. Sirve para llevar la configuración a otro PC o después de formatear.

## Buscar y filtrar (disco, tamaño)

- **Búsqueda:** busca en nombre, descripción, ubicación, categoría, subcategoría, fabricante, notas y etiquetas (también en los nombres y descripciones traducidos, en el idioma elegido). Los recuentos del panel izquierdo se ajustan.
- **Disco:** lista solo los programas instalados en C:, D:, F:, etc. (las letras aparecen según su PC).
- **Tamaño:** menos de 100 MB, más de 100 MB, 500 MB, 1 GB o 5 GB. Los programas cuyo tamaño aún es «…» (en cálculo) quedan fuera de estos filtros.
- **Limpiar filtros** lo devuelve todo a la normalidad. La búsqueda y los filtros valen juntos y también para la **exportación**.

## Programas que se abren con .bat (portátiles)

Algunos programas no tienen instalador ni acceso directo: usted abre un `run.bat` o `start.bat` dentro de la carpeta (habitual en herramientas portátiles y de IA). El escaneo busca esos archivos `.bat` y `.cmd` y muestra cada **carpeta como un elemento**, en la categoría **Programas sin instalador** (o en otra categoría, si el catálogo conoce el programa).

- **Dónde busca:** Descargas, Escritorio, Documentos y los discos que no son el de Windows (D:, F:…), hasta 3 o 4 niveles de carpetas. Para incluir otra carpeta, ponga la ruta en `categories.local.json`, en `"launchers": {"raizes_extra": ["E:\\Programas"]}`, y reescanee.
- **Qué archivos cuenta:** nombres de inicio (`run`, `start`, `launch`, `iniciar`, `abrir`, `webui`…), o el único `.bat` de una carpeta. Ignora instaladores, scripts de prueba y de compilación, y carpetas internas (`venv`, `node_modules`, `bin`, `python_embeded`…), además de las carpetas de programas que ya aparecen por el menú Inicio.
- **Variantes:** si la carpeta tiene varios launchers (`run.bat`, `run_anime.bat`…), el elemento abre el principal y el clic derecho > **Abrir variante** lista los demás.
- El `.bat` se ejecuta en su propia carpeta, en una ventana de consola. Los programas así no tienen desinstalador: para quitarlos, use **Abrir carpeta** y borre la carpeta desde el Explorador.
- Puede aparecer algo que no es exactamente un programa (script suelto, herramienta de desarrollo). Use **Ocultar** en esos casos.
- El escaneo se vuelve más lento (unos 1 min 30 s) por esta búsqueda en los discos.

## Añadir y ocultar elementos

- **Añadir…** (botón del pie): elija un `.exe`, `.bat`, `.cmd`, `.ps1`, `.py`, `.jar` o `.lnk` que el escaneo no encontró. Indique el nombre y, si quiere, para qué sirve. Entra en *Programas sin instalador › Añadidos por mí*. Para quitarlo: clic derecho > **Quitar elemento que añadí** (no borra los archivos).
- **Ocultar de la lista** (clic derecho): esconde un elemento de todas las pantallas y recuentos. Los ocultos quedan en la categoría **Ocultos**, donde el clic derecho ofrece **Mostrar de nuevo en la lista**.
- Ambas se pueden deshacer (Ctrl+Z o Historial) y sobreviven al reescaneo.

## Abrir programas

- Doble clic, `Enter` o botón **Abrir:** abre el programa (por el acceso directo del menú Inicio, cuando existe; los scripts `.bat` se ejecutan en su propia carpeta).
- **Abrir carpeta:** abre la carpeta de instalación en el Explorador.
- **★ Favorito:** marca o desmarca el elemento seleccionado.

## Menú del clic derecho

- **Abrir**, **Abrir carpeta**, **Añadir a / Quitar de favoritos**, **Abrir variante** (cuando la carpeta tiene varios `.bat`).
- **Ocultar de la lista** / **Mostrar de nuevo en la lista** y **Quitar elemento que añadí**: vea «Añadir y ocultar elementos».
- **Notas y etiquetas…**, y **Actualizar a… (winget)** cuando hay versión nueva.
- **Editar descripción…:** cambia el texto de «para qué sirve» (se guarda en `user.json`). Déjelo en blanco para volver al original.
- **Desinstalar…:** vea la sección siguiente.
- **Mover a categoría:** elija la categoría y la subcategoría, o cree nuevas («Nueva subcategoría…», «Nueva categoría…»). Se guarda en `categories.local.json` y vale para los próximos escaneos.
- **Enviar acceso directo roto a la Papelera…:** solo aparece en accesos directos rotos. Pide confirmación, guarda una copia del acceso directo y lo envía a la Papelera (no se borra definitivamente).

## Desinstalar (pide contraseña)

El botón **Desinstalar…** (o el menú del clic derecho) usa el desinstalador que el propio Windows tiene registrado para el programa.

1. La aplicación muestra el nombre registrado y el comando que va a ejecutar, y pide confirmación.
2. Pregunta si quiere **crear un punto de restauración de Windows** antes. Con él puede volver atrás desde Windows (Restaurar sistema). Exige la *Protección del sistema* activada; si no se puede crear, no se desinstala nada.
3. Windows pide la **confirmación de administrador (contraseña)** y se ejecuta el desinstalador.
4. Al terminar, la aplicación ofrece reescanear la lista.

> **Atención:** la aplicación **no puede revertir** una desinstalación. La única forma de volver atrás es el punto de restauración de Windows o reinstalar el programa.

Precauciones:

- Varios accesos directos pueden pertenecer al mismo programa (por ejemplo, Word, Excel y Outlook pertenecen a Office; LibreOffice Calc y Writer, a LibreOffice). Desinstalar cualquiera elimina el **conjunto completo**, y la aplicación avisa cuando el nombre registrado es distinto del elemento.
- Programas portátiles, sin desinstalador registrado: la aplicación ofrece abrir «Aplicaciones instaladas» de Windows.
- Un acceso directo roto no tiene nada que desinstalar.

## Deshacer e historial

- **Deshacer (Ctrl+Z)** revierte la última acción reversible. **Historial…** lista las acciones y permite revertir cualquiera de ellas.
- Se pueden deshacer: marcar/desmarcar favorito, editar descripción, mover de categoría, ocultar/mostrar, añadir/quitar un elemento manual, editar notas y etiquetas, restaurar una copia de seguridad y enviar un acceso directo roto a la Papelera (la aplicación restaura la copia que guardó en `backup/atalhos`; si la carpeta exige permiso, pide confirmación de administrador).
- **No** se pueden deshacer desde la aplicación: desinstalaciones y actualizaciones con winget (quedan registradas como «no reversible desde la aplicación»).

## Menús superiores

Los botones superiores ahora son menús (el menú del clic derecho y los botones del pie no cambian):

- **Archivo:** **Reescanear** (`F5`; rehace el escaneo en cerca de 1 min, la lista aparece enseguida y los tamaños se van rellenando), **Exportar…** (`Ctrl+E`; guarda la lista mostrada, con búsqueda y filtros, como CSV para Excel o como página HTML con búsqueda), **Guardar copia de la configuración…**, **Restaurar copia…** y **Salir** (`Ctrl+Q`).
- **Ver:** **Cambiar tema claro/oscuro** (al iniciar, sigue el tema de Windows), **Columnas** (mostrar u ocultar) y **Limpiar filtros**.
- **Herramientas:** **Buscar actualizaciones**, **Resumen de los programas…**, **Añadir programa…**, **Deshacer** (`Ctrl+Z`) e **Historial de acciones…**.
- **🌐 Idioma:** elige Português, English o Español (vea «Idioma»).
- **Ayuda:** **Ayuda** (`F1`: esta ventana; **Ir al índice** vuelve al inicio y **Abrir archivo de ayuda** abre el archivo), **Abrir página del proyecto** (GitHub) y **Acerca de App-Manager…** (versión y licencia).

## Idioma

El menú **🌐 Idioma** (arriba) elige el idioma de la interfaz, de los nombres de categorías, de las descripciones «para qué sirve» del catálogo y de esta Ayuda: **Português, English y Español**. Al elegir, la aplicación se reabre sola.

- El inglés es el idioma predeterminado. La elección se guarda en `user.json`.
- No se traducen: nombres de programas, descripciones que usted escribió (Editar descripción…) y textos que vienen del propio programa (fabricante, descripción del archivo).
- Los textos traducidos están en `lang/en.json` y `lang/es.json`; esta Ayuda existe como `help/pt.md`, `help/en.md` y `help/es.md`.

## Atajos de teclado

- `Ctrl+F`: va a la búsqueda.
- `Flecha abajo` o `Enter` (en la búsqueda): pasa a la lista.
- `Esc` (en la búsqueda): borra la búsqueda.
- `Enter` o doble clic (en la lista): abre el programa.
- `Ctrl+Z`: deshace la última acción reversible.
- `F5`: reescanea.
- `Ctrl+E`: exporta la lista.
- `Ctrl+Q`: cierra la aplicación.
- `F1`: abre la ayuda.

## Versión .exe portátil

Además del código (`App-Manager.bat`), existe `App-Manager.exe`, que **no requiere Python**. Colóquelo en una carpeta donde pueda escribir (por ejemplo `D:\Apps\App-Manager`): crea al lado `index.json`, `user.json`, `icons/` y `backup/`. Si la carpeta no permite escribir, usa `%APPDATA%\App-Manager`. Para actualizar, cambie solo el `.exe`; sus datos se conservan. **Reescanear** ejecuta el propio `.exe`.

Windows (SmartScreen) o el antivirus pueden avisar, porque el `.exe` es nuevo y no tiene firma digital. Si lo prefiere, use la versión con Python.

## Archivos de la carpeta

- `index.json`: el índice generado por el escaneo.
- `categories.json`: el **catálogo** predeterminado (palabras del nombre → categoría, subcategoría y descripción) y las reglas de reserva; viene con la aplicación.
- `categories.local.json` (opcional, privado): **su** catálogo, las categorías que usted movió, carpetas extra para programas `.bat` y `limpeza_dias`. Mismo formato que `categories.json`; sus entradas ganan. `lang.local.en.json` / `lang.local.es.json` (opcionales) guardan sus traducciones.
- `user.json`: sus favoritos, recuento y fecha de aperturas, descripciones, notas, etiquetas, elementos ocultos, elementos añadidos, columnas elegidas, idioma y el historial de acciones.
- `updates.json`: resultado de la última comprobación de winget. `usage.py`: lectura del uso, del inicio y de winget.
- `backup/atalhos/`: copias de los accesos directos enviados a la Papelera (usadas por Deshacer).
- `icons/`: iconos extraídos de los programas.
- `scan.py` (escaneo), `app.py` (la ventana), `usage.py`, `i18n.py`, `paths.py` y `version.py` (apoyo), `lang/` (traducciones), `help/` (esta Ayuda, en 3 idiomas), `assets/` (logo e icono) y `App-Manager.bat` (para abrir).

## Consejos y límites

- Los programas de la Microsoft Store (UWP) y los elementos sin ejecutable propio no aparecen.
- El tamaño es el de toda la carpeta de instalación; los programas en carpetas de Windows muestran solo el tamaño del ejecutable.
- Los programas que no están en el catálogo caen en «Otros» o en una regla de reserva y pueden quedar sin descripción: use el clic derecho para corregir.
- Para enseñar al catálogo, edite `categories.local.json` (lista `catalogo`: `k` = partes del nombre, `c` = categoría, `s` = subcategoría, `d` = descripción; `=nombre` exige nombre exacto) y reescanee. Las descripciones que añada se muestran tal como las escribe (en portugués, salvo que las escriba en su idioma).
- Los accesos directos rotos son solo un aviso: compruebe antes de enviarlos a la Papelera.
