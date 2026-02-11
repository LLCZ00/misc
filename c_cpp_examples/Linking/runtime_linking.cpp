/* *
 * Windows API Tests
 * */

#include <Windows.h>

using protobox = int (WINAPI *)(HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType);

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE nothin, PSTR cmdline, int cmdshow)
{
    //HMODULE user32 = LoadLibraryExA("user32.dll", nullptr, LOAD_LIBRARY_SEARCH_SYSTEM32);
    HMODULE user32 = LoadLibraryA("user32.dll");
    if (user32 == nullptr) { return 1; }

    auto box = (protobox)GetProcAddress(user32, "MessageBoxA");
    if (box == nullptr) { FreeLibrary(user32); return 2; }

    box(nullptr, "runtime box", "runtime caption", 4);

    FreeLibrary(user32);
    return 0;
}

/* Alternatively */
#include <cstdio>
#include <windows.h>

int main()
{
    HMODULE mylib = LoadLibraryA("TestDLL.dll");
    if (mylib == NULL) { puts("Failed to load library"); exit(1); }

    auto myfunction = GetProcAddress(mylib, "ServiceMain");
    if (myfunction == NULL) { puts("Failed to load function"); FreeLibrary(mylib); exit(1); }

    (void (CALLBACK*)(void))(myfunction)(); // Call function with casting shenanigans

    FreeLibrary(mylib);
    return 0;
}

/* Not using "using" */
int main()
{
	HMODULE kernel32 = GetModuleHandle("kernel32.dll");
	printf("Kernel32 Address: 0x%08p\n", kernel32);
	
	FARPROC winExecAddr = GetProcAddress(kernel32, "WinExec");
	printf("WinExec Address: 0x%08p\n", winExecAddr);
	
	UINT (WINAPI *myexec)(LPCSTR, UINT);
	myexec = (UINT (WINAPI *)(LPCSTR, UINT)) winExecAddr;
	myexec("C:\\Windows\\System32\\calc.exe", 1);
	
	return 0;
}