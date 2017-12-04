@ECHO OFF
cd %~dp0
:: https://stackoverflow.com/questions/15567809/batch-extract-path-and-filename-from-a-variable
for %%A IN (%~dp0\cards\bin\*.bin) DO nedcenc.exe -e -i "%%A" -o "%~dp0\cards\raw\%%~nA-hax.raw"