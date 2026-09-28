; FotoFacile — script di installazione per Inno Setup 6
;
; Serve a creare un vero programma di installazione per Windows:
;   FotoFacile-Setup-<versione>.exe
; che installa l'eseguibile, crea i collegamenti e registra la disinstallazione in
; «App e funzionalità». Si compila con:
;   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\windows\FotoFacile.iss
; (è quello che fa la pipeline GitHub su un computer Windows: vedi .github/workflows)

#define NomeApp "FotoFacile"
#define Versione "0.1.0"
#define Editore "FotoFacile"
#define Sito "https://github.com/marcosalvatori0/fotofacile"
#define Eseguibile "FotoFacile.exe"
#define CartellaSorgente "..\..\dist\FotoFacile"

[Setup]
AppId={{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}
AppName={#NomeApp}
AppVersion={#Versione}
AppVerName={#NomeApp} {#Versione}
AppPublisher={#Editore}
AppPublisherURL={#Sito}
AppSupportURL={#Sito}
AppUpdatesURL={#Sito}
DefaultDirName={autopf}\{#NomeApp}
DefaultGroupName={#NomeApp}
DisableProgramGroupPage=yes
; installazione per l'utente corrente: nessun privilegio di amministratore
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\..\dist\installer
OutputBaseFilename={#NomeApp}-Setup-{#Versione}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayName={#NomeApp}
UninstallDisplayIcon={app}\{#Eseguibile}
LicenseFile=..\..\LEGGIMI - Installazione.txt
InfoBeforeFile=..\..\LEGGIMI - Installazione.txt
SetupIconFile=..\..\assets\fotofacile.ico
ShowLanguageDialog=auto
DisableWelcomePage=no

[Languages]
Name: "italiano"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "Crea un collegamento sul Desktop"; GroupDescription: "Collegamenti:"; Flags: checkedonce
Name: "startmenuicon"; Description: "Crea un collegamento nel menu Start"; GroupDescription: "Collegamenti:"

[Files]
Source: "{#CartellaSorgente}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#NomeApp}"; Filename: "{app}\{#Eseguibile}"; Tasks: startmenuicon; Comment: "Copia le foto dal telefono Android al computer"
Name: "{autodesktop}\{#NomeApp}"; Filename: "{app}\{#Eseguibile}"; Tasks: desktopicon; Comment: "Copia le foto dal telefono Android al computer"

[Run]
Filename: "{app}\{#Eseguibile}"; Description: "Avvia {#NomeApp}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\{#Eseguibile}"; Parameters: "doctor"; Description: "Mostra la diagnosi del computer"; Flags: nowait postinstall skipifsilent unchecked

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
