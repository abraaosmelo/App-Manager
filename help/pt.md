# App-Manager — Ajuda

## Índice

- [O que é](#o-que-e)
- [Navegar: categorias e subcategorias](#navegar-categorias-e-subcategorias)
- [Colunas: último uso, vezes usado, instalado em](#colunas-ultimo-uso-vezes-usado-instalado-em)
- [Categorias especiais](#categorias-especiais)
- [Sugestão de limpeza](#sugestao-de-limpeza)
- [Iniciam com o Windows](#iniciam-com-o-windows)
- [Atualizações (winget)](#atualizacoes-winget)
- [Versões duplicadas](#versoes-duplicadas)
- [Notas e tags](#notas-e-tags)
- [Resumo](#resumo)
- [Backup da configuração](#backup-da-configuracao)
- [Buscar e filtrar (disco, tamanho)](#buscar-e-filtrar-disco-tamanho)
- [Programas que abrem por .bat (portáteis)](#programas-que-abrem-por-bat-portateis)
- [Adicionar e ocultar itens](#adicionar-e-ocultar-itens)
- [Abrir programas](#abrir-programas)
- [Menu do botão direito](#menu-do-botao-direito)
- [Desinstalar (pede senha)](#desinstalar-pede-senha)
- [Desfazer e histórico](#desfazer-e-historico)
- [Menus do topo](#menus-do-topo)
- [Idioma](#idioma)
- [Atalhos de teclado](#atalhos-de-teclado)
- [Versão .exe (portátil)](#versao-exe-portatil)
- [Arquivos da pasta](#arquivos-da-pasta)
- [Dicas e limites](#dicas-e-limites)

## O que é

Índice dos programas instalados neste PC, montado a partir dos **atalhos do Menu Iniciar** (e de alguns programas do registro do Windows que não têm atalho). Para cada um mostra nome, versão, local de instalação, tamanho, disco, categoria e **para que serve**.

Para abrir: duplo clique em `App-Manager.bat` (ou em `App-Manager.exe`, na versão portátil; veja "Versão .exe (portátil)").

O app só lê informações. Ele só altera algo quando você manda: desinstalar, mandar atalho quebrado para a Lixeira, mover de categoria etc.

## Navegar: categorias e subcategorias

- **Painel esquerdo:** categorias com a contagem de programas. Clique na seta para abrir as **subcategorias** (por exemplo, Desenvolvimento › Editores e IDEs).
- **Painel direito:** lista com ícone, nome, versão, tamanho, disco, categoria › subcategoria e local. Clique no título de uma coluna para ordenar.
- **Rodapé:** detalhes do item selecionado (categoria, disco, versão, fabricante, quantas vezes foi aberto por aqui, tamanho, local, se há desinstalador e para que serve).
- **Barra de status** (canto superior direito): total exibido, "calculando tamanhos…", quanto tempo faz o último scan ("escaneado há 5 min"; se estiver velho, use Reescanear), novos e removidos.

## Colunas: último uso, vezes usado, instalado em

A tabela tem estas colunas (clique com o **botão direito no título** de qualquer coluna para mostrar ou esconder; há "Restaurar colunas padrão"; a tabela ganha rolagem horizontal se não couber): Nome, Versão, Atualização, Tamanho, Disco, **Último uso**, **Vezes usado**, **Instalado em**, Inicia com Windows, Tags, Categoria › Subcategoria e Local. Clique no título para ordenar.

- **Último uso e Vezes usado:** vêm do registro do Windows (UserAssist), que anota quando você abre um programa pelo Explorer, Menu Iniciar, barra de tarefas ou área de trabalho. Somam-se às aberturas feitas por este índice (vale o maior número, para não contar duas vezes). Os dados são lidos de novo toda vez que você volta para a janela. A coluna Último uso se alarga sozinha para caber o texto mais longo.
- **"sem registro"** significa que o Windows não anotou nenhuma abertura. Isso **não prova** que o programa nunca foi usado: o Windows não registra programas abertos por linha de comando, por scripts `.bat`, por serviços ou pelo Gerenciador de Tarefas, e o histórico só existe desde que o recurso foi ativado.
- **Instalado em:** data de instalação do registro do Windows quando existe; senão, a data de criação da pasta do programa (pode ser a data em que a pasta foi copiada).

## Categorias especiais

- **Todos:** tudo o que foi encontrado.
- **★ Favoritos:** os programas que você marcou.
- **Mais usados:** os 15 com mais aberturas (registro do Windows + este índice).
- **Novos desde o último scan:** programas que apareceram depois do scan anterior (marcados com "(novo)").
- **Sem atalho no Menu Iniciar:** programas instalados que não têm atalho, mas têm executável que dá para abrir.
- **Sugestão de limpeza, Iniciam com o Windows, Com atualização e Versões duplicadas:** veja as seções abaixo.
- **Tags:** aparece quando você cria tags; cada tag vira um filtro.
- **Ocultos:** aparece só quando você ocultou algum item (veja "Adicionar e ocultar itens").
- **Atalhos quebrados:** atalhos cujo programa não existe mais (provavelmente desinstalado). As subcategorias dela mostram o tipo do programa que era.

## Sugestão de limpeza

Lista os programas **sem uso há 180 dias ou mais, ou sem registro de uso**, do maior para o menor, e a barra de status mostra quanto espaço isso poderia liberar (pastas contadas uma vez). Ficam de fora: categoria Sistema, atalhos quebrados e seus favoritos.

É só uma sugestão. Como "sem registro" pode ser um programa que você usa por outros caminhos, confira cada item antes de usar **Desinstalar…**. Para mudar o prazo, coloque `"limpeza_dias": 365` em `categories.local.json` e reabra o app.

## Iniciam com o Windows

Mostra os programas que abrem sozinhos ao ligar o PC, lidos das chaves *Run* do registro e da pasta Inicializar. A coluna **Inicia com Windows** indica **Sim** ou **Desativado** (quando você já desligou no Gerenciador de Tarefas); a categoria lista só os ativos. O app apenas mostra: para ligar ou desligar, use a aba Inicializar do Gerenciador de Tarefas. A ligação entre a entrada e o programa é por caminho do executável ou pela pasta de instalação, então pode listar vários atalhos do mesmo programa.

## Atualizações (winget)

- **Ferramentas › Verificar atualizações** consulta o `winget` do Windows (cerca de 15 s) e guarda o resultado em `updates.json`.
- Itens com versão nova ganham a coluna **Atualização** (→ versão), a categoria **Com atualização** e a linha de detalhe. O botão **Atualizar…** (ou botão direito) executa `winget upgrade` numa janela de console, com confirmação; o Windows pode pedir senha de administrador.
- O app **não consegue desfazer** uma atualização. Quando a janela do winget fecha, o app consulta o winget de novo (sem mensagem) e tira da lista o que já foi atualizado. Para a coluna Versão mostrar a versão nova, clique em Reescanear.
- Só aparecem programas que o winget conhece e que casam com o nome do item; componentes do Windows, drivers e apps da Loja ficam de fora.

## Versões duplicadas

A categoria **Versões duplicadas** agrupa itens parecidos, por exemplo vários Pythons, dois Visual Studios ou os atalhos "x86" e "x64". O detalhe mostra o grupo e o espaço total. Serve para decidir o que desinstalar; nem todo grupo é um problema (atalhos do mesmo programa também entram).

## Notas e tags

**Notas e tags…** (botão do rodapé ou botão direito) abre uma janela para escrever anotações (licença, onde baixou, projeto) e tags separadas por vírgula. As tags aparecem na categoria **Tags** (um filtro por tag) e na coluna Tags; busca também procura em notas e tags. Dá para desfazer.

## Resumo

O menu **Ferramentas › Resumo dos programas…** abre uma tela com: número de programas e espaço total, sugestão de limpeza, quantos iniciam com o Windows e têm atualização, grupos duplicados, espaço por categoria e por disco, os 10 maiores, os 10 mais usados e instalações por ano. Itens ocultos e atalhos quebrados não entram.

## Backup da configuração

**Arquivo › Salvar backup da configuração…** salva num arquivo `.json` tudo o que é seu: favoritos, contagem e data de uso, descrições editadas, notas, tags, itens ocultos, itens adicionados, colunas escolhidas e categorias movidas. **Arquivo › Restaurar backup…** pergunta se deve **mesclar** com o que existe ou **substituir**; antes disso o app guarda uma cópia do estado atual em `backup/` e dá para **desfazer** pelo Histórico. Serve para levar a configuração a outro PC ou depois de formatar.

## Buscar e filtrar (disco, tamanho)

- **Busca:** procura no nome, descrição, local, categoria, subcategoria, fabricante, notas e tags (também nos nomes e descrições traduzidos, no idioma escolhido). As contagens do painel esquerdo se ajustam.
- **Disco:** lista só os programas instalados em C:, D:, F: etc. (as letras aparecem conforme o seu PC).
- **Tamanho:** menor que 100 MB, maior que 100 MB, 500 MB, 1 GB ou 5 GB. Programas com tamanho ainda "…" (sendo calculado) ficam de fora desses filtros.
- **Limpar filtros** volta tudo ao normal. A busca e os filtros valem juntos e também para a **exportação**.

## Programas que abrem por .bat (portáteis)

Alguns programas não têm instalador nem atalho: você abre um `run.bat` ou `start.bat` dentro da pasta (comum em ferramentas portáteis e de IA). O scan procura esses arquivos `.bat` e `.cmd` e mostra cada **pasta como um item**, na categoria **Programas sem instalador** (ou em outra categoria, se o catálogo conhecer o programa).

- **Onde procura:** Downloads, Desktop, Documentos e os discos que não são o do Windows (D:, F:…), até 3 ou 4 níveis de pasta. Para incluir outra pasta, coloque o caminho em `categories.local.json`, em `"launchers": {"raizes_extra": ["E:\\Programas"]}`, e reescaneie.
- **Quais arquivos conta:** nomes de inicialização (`run`, `start`, `launch`, `iniciar`, `abrir`, `webui`…), ou o único `.bat` de uma pasta. Ignora instaladores, scripts de teste e de build, e pastas internas (`venv`, `node_modules`, `bin`, `python_embeded`…), além das pastas de programas que já aparecem pelo Menu Iniciar.
- **Variantes:** se a pasta tem vários launchers (`run.bat`, `run_anime.bat`…), o item abre o principal e o botão direito > **Abrir variante** lista os outros.
- O `.bat` roda na própria pasta, em uma janela de console. Programas assim não têm desinstalador: para remover, use **Abrir pasta** e apague a pasta pelo Explorer.
- Pode aparecer coisa que não é bem um programa (script solto, ferramenta de desenvolvimento). Use **Ocultar** nesses casos.
- O scan fica mais demorado (cerca de 1 min 30 s) por causa dessa busca nos discos.

## Adicionar e ocultar itens

- **Adicionar…** (botão no rodapé): escolha um `.exe`, `.bat`, `.cmd`, `.ps1`, `.py`, `.jar` ou `.lnk` que o scan não achou. Informe o nome e, se quiser, para que serve. Entra em *Programas sem instalador › Adicionados por mim*. Para tirar: botão direito > **Remover item adicionado por mim** (não apaga os arquivos).
- **Ocultar da lista** (botão direito): esconde um item de todas as telas e contagens. Os ocultos ficam na categoria **Ocultos**, onde o botão direito oferece **Mostrar de novo na lista**.
- Os dois podem ser desfeitos (Ctrl+Z ou Histórico) e sobrevivem ao reescaneamento.

## Abrir programas

- Duplo clique, `Enter` ou botão **Abrir:** abre o programa (pelo atalho do Menu Iniciar, quando existe; scripts `.bat` rodam na própria pasta).
- **Abrir pasta:** abre a pasta de instalação no Explorer.
- **★ Favorito:** marca ou desmarca o item selecionado.

## Menu do botão direito

- **Abrir**, **Abrir pasta**, **Adicionar/Remover dos favoritos**, **Abrir variante** (quando a pasta tem vários `.bat`).
- **Ocultar da lista** / **Mostrar de novo na lista** e **Remover item adicionado por mim**: veja "Adicionar e ocultar itens".
- **Notas e tags…**, e **Atualizar para… (winget)** quando há versão nova.
- **Editar descrição…:** troca o texto de "para que serve" (fica em `user.json`). Deixe em branco para voltar ao original.
- **Desinstalar…:** veja a seção abaixo.
- **Mover para categoria:** escolha a categoria e a subcategoria, ou crie novas ("Nova subcategoria…", "Nova categoria…"). Fica salvo em `categories.local.json` e vale nos próximos scans.
- **Enviar atalho quebrado para a Lixeira…:** só aparece em atalhos quebrados. Pede confirmação, guarda uma cópia do atalho e manda para a Lixeira (não apaga de vez).

## Desinstalar (pede senha)

O botão **Desinstalar…** (ou o menu do botão direito) usa o desinstalador que o próprio Windows tem registrado para o programa.

1. O app mostra o nome registrado e o comando que vai rodar, e pede confirmação.
2. Pergunta se você quer **criar um ponto de restauração do Windows** antes. Com ele você pode voltar atrás pelo Windows (Restauração do Sistema). Exige a *Proteção do Sistema* ativada; se não der para criar, nada é desinstalado.
3. O Windows pede a **confirmação de administrador (senha)**, e o desinstalador roda.
4. Ao terminar, o app oferece reescanear a lista.

> **Atenção:** o app **não consegue reverter** uma desinstalação. O único jeito de voltar atrás é o ponto de restauração do Windows ou reinstalar o programa.

Cuidados:

- Vários atalhos podem pertencer ao mesmo programa (por exemplo, Word, Excel e Outlook pertencem ao Office; LibreOffice Calc e Writer, ao LibreOffice). Desinstalar qualquer um remove o **conjunto inteiro**, e o app avisa quando o nome registrado é diferente do item.
- Programas portáteis, sem desinstalador registrado: o app oferece abrir "Aplicativos instalados" do Windows.
- Atalho quebrado não tem o que desinstalar.

## Desfazer e histórico

- **Desfazer (Ctrl+Z)** reverte a última ação reversível. **Histórico…** lista as ações e deixa reverter qualquer uma delas.
- Podem ser desfeitos: marcar/desmarcar favorito, editar descrição, mover de categoria, ocultar/mostrar, adicionar/remover item manual, editar notas e tags, restaurar um backup e enviar atalho quebrado à Lixeira (o app restaura a cópia que guardou em `backup/atalhos`; se a pasta exigir permissão, pede confirmação de administrador).
- **Não** podem ser desfeitos pelo app: desinstalações e atualizações pelo winget (ficam registradas como "irreversível pelo app").

## Menus do topo

Os botões do topo viraram menus (o menu do botão direito e os botões do rodapé continuam iguais):

- **Arquivo:** **Reescanear** (`F5`; refaz a varredura em cerca de 1 min, a lista aparece logo e os tamanhos vão sendo preenchidos), **Exportar…** (`Ctrl+E`; salva a lista exibida, com busca e filtros, como CSV para o Excel ou como página HTML com busca), **Salvar backup da configuração…**, **Restaurar backup…** e **Sair** (`Ctrl+Q`).
- **Exibir:** **Alternar tema claro/escuro** (ao iniciar, segue o tema do Windows), **Colunas** (mostrar ou esconder) e **Limpar filtros**.
- **Ferramentas:** **Verificar atualizações**, **Resumo dos programas…**, **Adicionar programa…**, **Desfazer** (`Ctrl+Z`) e **Histórico de ações…**.
- **🌐 Idioma:** escolhe Português, English, Español, Français ou Deutsch (veja "Idioma").
- **Ajuda:** **Ajuda** (`F1`: esta janela; **Ir ao índice** volta ao topo e **Abrir arquivo de ajuda** abre o arquivo), **Abrir página do projeto** (GitHub) e **Sobre o App-Manager…** (versão e licença).

## Idioma

O menu **🌐 Idioma** (no topo) escolhe o idioma da interface, dos nomes das categorias, das descrições "para que serve" do catálogo e desta Ajuda: **Português, English, Español, Français e Deutsch**. Ao escolher, o app reabre sozinho.

- O padrão é o inglês. A escolha fica em `user.json`.
- Não são traduzidos: nomes de programas, descrições que você escreveu (Editar descrição…) e textos que vêm do próprio programa (fabricante, descrição do arquivo).
- Os textos traduzidos ficam em `lang/en.json`, `lang/es.json`, `lang/fr.json` e `lang/de.json`; esta Ajuda existe como `help/pt.md`, `help/en.md`, `help/es.md`, `help/fr.md` e `help/de.md`.

## Atalhos de teclado

- `Ctrl+F`: vai para a busca.
- `Seta para baixo` ou `Enter` (na busca): passa para a lista.
- `Esc` (na busca): limpa a busca.
- `Enter` ou duplo clique (na lista): abre o programa.
- `Ctrl+Z`: desfaz a última ação reversível.
- `F5`: reescaneia.
- `Ctrl+E`: exporta a lista.
- `Ctrl+Q`: fecha o app.
- `F1`: abre a ajuda.

## Versão .exe (portátil)

Além do código (`App-Manager.bat`), há o `App-Manager.exe`, que **não exige Python**. Coloque-o numa pasta onde você possa gravar (por exemplo `D:\Apps\App-Manager`): ele cria ao lado `index.json`, `user.json`, `icons/` e `backup/`. Se a pasta não permitir gravar, ele usa `%APPDATA%\App-Manager`. Para atualizar, troque só o `.exe`; seus dados ficam. O **Reescanear** roda o próprio `.exe`.

O Windows (SmartScreen) ou o antivírus pode alertar, porque o `.exe` é novo e não tem assinatura digital. Se preferir, use a versão com Python.

## Arquivos da pasta

- `index.json`: o índice gerado pelo scan.
- `categories.json`: o **catálogo** padrão (palavras do nome → categoria, subcategoria e descrição) e as regras de reserva; vem com o app.
- `categories.local.json` (opcional, privado): **o seu** catálogo, as categorias que você moveu, pastas extras para programas `.bat` e `limpeza_dias`. Mesmo formato do `categories.json`; as suas entradas vencem. `lang.local.<idioma>.json` (opcionais, ex.: `lang.local.fr.json`) guardam as suas traduções.
- `user.json`: seus favoritos, contagem e data de aberturas, descrições, notas, tags, itens ocultos, itens adicionados, colunas escolhidas e o histórico de ações.
- `updates.json`: resultado da última verificação do winget. `usage.py`: leitura do uso, da inicialização e do winget.
- `backup/atalhos/`: cópias dos atalhos enviados à Lixeira (usadas pelo Desfazer).
- `icons/`: ícones extraídos dos programas.
- `scan.py` (varredura), `app.py` (a janela), `usage.py`, `i18n.py`, `paths.py` e `version.py` (apoio), `lang/` (traduções), `help/` (esta Ajuda, nos 5 idiomas), `assets/` (logo e ícone) e `App-Manager.bat` (para abrir).

## Dicas e limites

- Programas da Microsoft Store (UWP) e itens sem executável próprio não aparecem.
- O tamanho é o da pasta de instalação inteira; programas em pastas do Windows mostram só o tamanho do executável.
- Os programas que não estão no catálogo caem em "Outros" ou numa regra de reserva e podem ficar sem descrição: use o botão direito para corrigir.
- Para ensinar o catálogo, edite `categories.local.json` (lista `catalogo`: `k` = trechos do nome, `c` = categoria, `s` = subcategoria, `d` = descrição; `=nome` exige nome exato) e reescaneie.
- Atalhos quebrados são só um aviso: confira antes de mandar para a Lixeira.
