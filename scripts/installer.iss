; Inno Setup script para empacotar o binário Windows com dataset offline.
; Pré-requisitos:
; 1) Gerar o executável com PyInstaller (ex.: scripts/run_api.py).
;    pyinstaller --noconfirm --onedir ^
;      --add-data "data\\poems.csv;data" ^
;      --name "poesia-buscador" scripts\\run_api.py
; 2) A saída ficará em dist\\poesia-buscador\\ (inclui data\\poems.csv).
;
; Depois, rode este instalador no Inno Setup:
; iscc scripts\\installer.iss

[Setup]
AppName=Poesia Buscador
AppVersion=1.0.0
DefaultDirName={pf}\\PoesiaBuscador
DefaultGroupName=Poesia Buscador
OutputDir=dist\\installer
OutputBaseFilename=poesia-buscador-setup
Compression=lzma
SolidCompression=yes

[Files]
; Copia o executável e dependências geradas pelo PyInstaller
Source: "dist\\poesia-buscador\\*"; DestDir: "{app}"; Flags: recursesubdirs
; Dataset offline incluído no pacote (já vem de --add-data)
Source: "dist\\poesia-buscador\\data\\poems.csv"; DestDir: "{app}\\data"; Flags: ignoreversion

[Icons]
Name: "{group}\\Poesia Buscador (API)"; Filename: "{app}\\poesia-buscador.exe"
Name: "{commondesktop}\\Poesia Buscador (API)"; Filename: "{app}\\poesia-buscador.exe"

[Run]
Filename: "{app}\\poesia-buscador.exe"; Description: "Iniciar API agora"; Flags: nowait postinstall skipifsilent
