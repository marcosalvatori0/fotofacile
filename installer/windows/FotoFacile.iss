; FotoFacile — programma di installazione per Windows (Inno Setup 6)
;
; Crea  dist\installer\FotoFacile-Setup-<versione>.exe  con una procedura guidata in
; italiano: installa il programma, crea i collegamenti e registra la disinstallazione in
; «App e funzionalità». Non richiede i diritti di amministratore.
;
; Si compila su Windows (lo fa la pipeline GitHub, vedi .github/workflows):
;   ISCC.exe /DVersione=0.2.0 installer\windows\FotoFacile.iss

#ifndef Versione
  #define Versione "0.2.0"
#endif
#define NomeApp "FotoFacile"
#define Editore "FotoFacile"
#define Sito "https://github.com/marcosalvatori0/fotofacile"
#define Eseguibile "FotoFacile.exe"
#define CartellaSorgente "..\..\dist\FotoFacile"

[Setup]
; NON cambiare mai l'AppId: serve a riconoscere una versione già installata e ad aggiornarla.
AppId={{8C1B7A54-6E1F-4A62-9E77-6A5B7C4C1F21}
AppName={#NomeApp}
AppVersion={#Versione}
AppVerName={#NomeApp} {#Versione}
AppPublisher={#Editore}
AppPublisherURL={#Sito}
AppSupportURL={#Sito}
AppUpdatesURL={#Sito}
VersionInfoVersion={#Versione}
VersionInfoDescription=Programma di installazione di {#NomeApp}
DefaultDirName={autopf}\{#NomeApp}
DisableProgramGroupPage=yes
DisableDirPage=auto
; installazione nel profilo dell'utente: nessun permesso di amministratore, nessuna domanda
PrivilegesRequired=lowest
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..\..\dist\installer
OutputBaseFilename={#NomeApp}-Setup-{#Versione}
Compression=lzma2
SolidCompression=yes
; finestra più grande e testo leggibile
WizardStyle=modern
WizardSizePercent=120,120
DisableWelcomePage=no
InfoBeforeFile=Benvenuto.txt
SetupIconFile=..\..\assets\fotofacile.ico
UninstallDisplayName={#NomeApp}
UninstallDisplayIcon={app}\{#Eseguibile}
; se il programma è aperto durante un aggiornamento, chiede di chiuderlo
CloseApplications=yes
RestartApplications=no
ShowLanguageDialog=no
LanguageDetectionMethod=none

[Languages]
Name: "italiano"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "Crea un'icona sul Desktop"; GroupDescription: "Collegamenti:"
Name: "startmenuicon"; Description: "Crea un collegamento nel menu Start"; GroupDescription: "Collegamenti:"

[Files]
Source: "{#CartellaSorgente}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\{#NomeApp}"; Filename: "{app}\{#Eseguibile}"; Tasks: desktopicon; Comment: "Copia le foto dal telefono Android al computer"
Name: "{autoprograms}\{#NomeApp}"; Filename: "{app}\{#Eseguibile}"; Tasks: startmenuicon; Comment: "Copia le foto dal telefono Android al computer"
Name: "{autoprograms}\{#NomeApp} - Diagnosi"; Filename: "{app}\{#Eseguibile}"; Parameters: "doctor"; Tasks: startmenuicon; Comment: "Se qualcosa non va: mostra un rapporto da mandare a chi ti aiuta"

[Run]
Filename: "{app}\{#Eseguibile}"; Description: "Apri {#NomeApp} adesso"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
// Alla disinstallazione si chiede se togliere anche le impostazioni e l'elenco dei file
// già copiati. Le FOTO copiate non si toccano mai.
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  CartellaDati: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    CartellaDati := ExpandConstant('{%USERPROFILE}\.fotofacile');
    if DirExists(CartellaDati) and (not UninstallSilent) then
    begin
      if MsgBox('Vuoi togliere anche le impostazioni e l''elenco delle foto già copiate?' + #13#10 +
                'Le foto copiate NON vengono cancellate.', mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
        DelTree(CartellaDati, True, True, True);
    end;
  end;
end;
