:: Building Executables without VS >:c

@echo off

set BIN=ctest.exe
set SOURCES=src\*.c
set VCBAT="C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"

if /I "%1" == "clean" (
	del .\%BIN% .\*.txt
) else (
	%comspec% /c "%VCBAT% amd64 && cl.exe %SOURCES% /link /out:%BIN%"
	del .\*.obj
)
