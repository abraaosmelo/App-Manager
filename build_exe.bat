@echo off
rem Gera dist\App-Manager.exe (precisa de Python; instala o PyInstaller se faltar).
cd /d "%~dp0"
python -m pip install --quiet pyinstaller || (echo Falha ao instalar o PyInstaller. & pause & exit /b 1)
python -m PyInstaller --noconfirm --clean --onefile --noconsole --name App-Manager --icon assets\icon.ico ^
  --hidden-import scan --add-data "lang;lang" --add-data "help;help" --add-data "assets;assets" ^
  --add-data "categories.json;." app.py || (echo Falha na geracao. & pause & exit /b 1)
echo.
echo Pronto: dist\App-Manager.exe
