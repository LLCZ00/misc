/* *
 * Windows API Tests
 * */

#include <Windows.h>
#include <iostream>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE nothin, PSTR cmdline, int cmdshow)
{
    if (AllocConsole() == 0) {return -1;}
    freopen_s((FILE **)stdin, "CONIN$", "r", stdin);
    freopen_s((FILE **)stdout, "CONOUT$", "w", stdout);
    freopen_s((FILE **)stderr, "CONERR$", "r", stderr);

    std::cout << cmdline;

    std::cout << "\nPress Enter to continue...";
    std::cin.ignore();
    FreeConsole();
    return 0;
}
