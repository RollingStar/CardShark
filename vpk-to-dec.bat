@ECHO OFF
:: https://stackoverflow.com/questions/11037831/filename-timestamp-in-windows-cmd-batch-script
for /f "tokens=2-8 delims=.:/ " %%a in ("%date% %time%") do set DateNtime=%%c-%%a-%%b_%%d-%%e-%%f-%%g
cd %~dp0
:: https://stackoverflow.com/questions/15567809/batch-extract-path-and-filename-from-a-variable
:: nevpk doesn't check for existing files before overwriting. give timestamp to help prevent overwriting wanted files
for %%A IN (%~dp0\cards\vpk\*.vpk) DO nevpk.exe -i "%%A" -o "%~dp0\cards\dec\%%~nA-%DateNtime%.dec" -v -d