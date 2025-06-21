;-------------------------------------------------------------------------------
; Installer.iss — Inno Setup Script for The Brain MQTT AUTO version 1.0
;-------------------------------------------------------------------------------

[Setup]
AppName=The Brain MQTT AUTO
AppVersion=1.0
DefaultDirName={pf}\TheBrainMQTTAuto
DefaultGroupName=TheBrainMQTTAuto
OutputBaseFilename=TheBrainMQTTAutoInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
SetupIconFile=static\The_Brain_MQTT_AUTO.ico

[Files]
; Bundle the Python installer into a subfolder
Source: "Python installer\python-3.13.5-amd64.exe"; DestDir: "{app}\Python installer"; Flags: ignoreversion
; Copy our Install.bat and config/template/static files
Source: "Install.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "mqtt_credentials.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "memory.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "The_Brain_MQTT_AUTO.py"; DestDir: "{app}"; Flags: ignoreversion ;
Source: "static\*"; DestDir: "{app}\static"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Shortcut to run the installer batch (which installs Python + venv + deps)
Name: "{group}\Install Dependencies"; Filename: "{app}\Install.bat"; WorkingDir: "{app}"; IconFilename: "{app}\static\The_Brain_MQTT_AUTO.ico"

; Wizard shortcut: launch the app via cmd.exe (so the icon sticks)
Name: "{group}\Launch The Brain"; Filename: "{cmd}"; Parameters: "/k cd /d ""%LOCALAPPDATA%\TheBrainMQTTAuto"" && call venv\Scripts\activate && python The_Brain_MQTT_AUTO.py"; WorkingDir: "{app}"; IconFilename: "{app}\static\The_Brain_MQTT_AUTO.ico"

; Optional desktop shortcut
Name: "{userdesktop}\The Brain"; Filename: "{cmd}"; Parameters: "/k cd /d ""%LOCALAPPDATA%\TheBrainMQTTAuto"" && call venv\Scripts\activate && python The_Brain_MQTT_AUTO.py"; Tasks: desktopicon; IconFilename: "{app}\static\The_Brain_MQTT_AUTO.ico"


[Tasks]
Name: desktopicon; Description: "Create a &desktop icon for The Brain"; GroupDescription: "Additional icons:"

[Run]
; After all files are copied, offer to run Install.bat
Filename: "{app}\Install.bat"; Description: "Run dependency installer now (Python + venv + deps)"; Flags: shellexec postinstall skipifsilent