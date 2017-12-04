@ECHO OFF
cd %~dp0
:: https://stackoverflow.com/questions/15567809/batch-extract-path-and-filename-from-a-variable
for %%A IN (%~dp0\cards\raw\*.raw) DO nedcenc.exe -d -i "%%A" -o "%~dp0\cards\bin\%%~nA.bin"