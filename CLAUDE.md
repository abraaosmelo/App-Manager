# App-Manager

App Tkinter (`app.py`) + varredura (`scan.py`) que cataloga os programas instalados no Windows (Menu Iniciar, registro, `.bat`). Abre com `App-Manager.bat` ou, na versão portátil, com `App-Manager.exe`. Só Windows 10/11. Repositório: https://github.com/thomasmeneghelli/App-Manager

## Regra obrigatória: manter a Ajuda atualizada (nos 4 idiomas)
A Ajuda do app fica em `help/pt.md`, `help/en.md`, `help/es.md` e `help/fr.md`, renderizada na janela "Ajuda" (menu Ajuda ou F1). Cada uma tem um **Índice** no topo com links `[Título](#slug)`; o slug é o título em minúsculas, sem acentos, com `-` no lugar de símbolos/espaços (ex.: "Desinstalar (pede senha)" → `#desinstalar-pede-senha`). As seções do corpo seguem a mesma ordem do Índice.

Sempre que mexer no app (menus, botões, filtros, atalhos de teclado, categorias, menu de contexto, desinstalação, desfazer, exportação, comportamento do scan, arquivos gerados), atualize **as quatro Ajudas na mesma alteração**: o texto da seção afetada e, se criar/renomear/remover seção, também o Índice. A tarefa só termina com a Ajuda refletindo o que mudou. Confira que cada link do Índice tem um título correspondente.

## Regra obrigatória: comentários do código em inglês
Comentários e docstrings dos `.py` (e `.bat`) são escritos em **inglês**. Textos visíveis ao usuário continuam em português dentro de `tr("...")` (a chave de tradução).

## Regra obrigatória: idiomas (português, English, Español, Français)
- Todo texto visível ao usuário no código entra por `tr("texto em português")` (`i18n.py`); a chave é o próprio texto em português, com `{campos}` e `.format` via `tr("...", campo=valor)`. Nunca monte frases com f-string sem `tr`.
- Texto novo precisa de tradução em `lang/en.json`, `lang/es.json` e `lang/fr.json` (seção `ui`). Nomes de categoria/subcategoria vão na seção `cat`; descrições do catálogo (`categories.json`, campo `d`) na seção `desc` (chave = texto exato em português); descrições geradas pelo scan, em `patterns`. Traduções do catálogo privado (`categories.local.json`) vão em `lang.local.<idioma>.json` (gitignored), nunca em `lang/`.
- Os dados guardados (`index.json`, `user.json`, `categories.json`) ficam sempre em português; só a exibição é traduzida (`tr`, `trc` para categorias, `trd` para descrições).
- Datas: `tr("%d/%m/%Y")` (inglês usa `%Y-%m-%d`).
- O idioma vale ao iniciar; a troca grava `idioma` em `user.json` e reabre o app.

## Estrutura
- `scan.py` — varre atalhos + registro do Windows, gera `index.json` e `icons/`; lê o desinstalador de cada programa. No `.exe` é chamado por `App-Manager.exe --scan`.
- `usage.py` — leituras somente-leitura usadas pelo app: uso (UserAssist), inicialização (Run), winget e versões duplicadas.
- `app.py` — janela (menus Arquivo/Exibir/Ferramentas/Idioma/Ajuda, tabela, diálogos); dados do usuário em `user.json` (favoritos, usos, descrições editadas, histórico para desfazer, idioma).
- `i18n.py` — `tr`/`trc`/`trd`, idioma atual (user.json; padrão English). `lang/en.json`, `lang/es.json`, `lang/fr.json` — traduções.
- `paths.py` — `APP` (dados do usuário, ao lado do script/.exe), `RES` (recursos embutidos no .exe) e migração dos nomes antigos (`indice.json`, `usuario.json`, `atualizacoes.json`, `categorias.json`).
- `version.py` — `APP_NAME`, `VERSION`, `REPO_URL` (suba a versão aqui).
- `categories.json` — catálogo PADRÃO e público: só programas comuns (Windows, Office, navegadores, dev, lojas de jogos…). Nunca coloque aqui apps pessoais ou de nicho.
- `config.py` + `categories.local.json` (privado, gitignored) — o catálogo do usuário: entradas extras, `overrides` (movidos pelo usuário, "Categoria > Subcategoria"), `launchers.raizes_extra`, `limpeza_dias`. `config.load()` mescla os dois (entradas locais vencem); o app só grava no local.
- `assets/` — `logo.svg`, `logo-64.png`, `logo-256.png`, `icon.ico`; gerados por `tools/make_logo.py`.
- `backup/atalhos/` — cópias de atalhos enviados à Lixeira (para Desfazer).
- `docs/screenshots/` — capturas do README, tiradas com dados FICTÍCIOS (nunca do seu próprio `index.json`); ficam fora de `assets/` para não entrarem no `.exe`.
- `build_exe.bat` — gera `dist\App-Manager.exe` com PyInstaller (`--onefile --noconsole`, embute `lang/`, `help/`, `assets/`, `categories.json`). Os subprocessos precisam de `stdin=DEVNULL` (sem console).

## Segurança
Desinstalar roda o desinstalador do registro com elevação (UAC pede senha). Nunca executar uma desinstalação nos testes; testar só até o diálogo/lógica de montagem.

## Publicação
Repositório público. Nunca versionar dados pessoais (`index.json`, `user.json`, `updates.json`, `icons/`, `backup/`, `categories.local.json`, `lang.local.*.json`, `*.lnk` e os nomes antigos): estão no `.gitignore`. O `.exe` vai em Releases, não no repositório.
