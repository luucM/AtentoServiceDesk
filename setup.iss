; =========================
; Inno Setup - Atento ServiceDesk
; =========================

[Setup]
AppName=Atento ServiceDesk
AppVersion=1.0
DefaultDirName=C:\AtentoBrasil\Atento ServiceDesk
DefaultGroupName=Atento ServiceDesk
OutputDir=dist
OutputBaseFilename=AtentoServiceDeskSetup
SetupIconFile=dist\icone.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
; Executável principal
Source: "dist\atentoservicedesk.exe"; DestDir: "{app}"; Flags: ignoreversion

; Script limpa temporários
Source: "limpa_temporarios.bat"; DestDir: "{app}"; Flags: ignoreversion

; Pasta de registros
Source: "regs\*"; DestDir: "{app}\regs"; Flags: recursesubdirs createallsubdirs

; Ícones usados na interface
Source: "icones\*"; DestDir: "{app}\icones"; Flags: recursesubdirs createallsubdirs

[Icons]
; Atalhos principais
Name: "{group}\Atento ServiceDesk"; Filename: "{app}\atentoservicedesk.exe"
Name: "{commondesktop}\Atento ServiceDesk"; Filename: "{app}\atentoservicedesk.exe"

[Run]
; Mostra a caixinha no final perguntando se deseja abrir o programa
Filename: "{app}\atentoservicedesk.exe"; Description: "Abrir Atento ServiceDesk"; Flags: nowait postinstall skipifsilent unchecked