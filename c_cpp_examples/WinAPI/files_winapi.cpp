/* *
 * Windows API Tests
 * */

#include <Windows.h>

// MessageBoxA(nullptr, "This is my window", "This is my caption", MB_CANCELTRYCONTINUE | MB_ICONASTERISK | MB_DEFBUTTON1);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE nothin, PSTR cmdline, int cmdshow)
{

    LPCSTR buffer = "booty-o's are part of a balance breakfast\n";

    HANDLE buttfile = CreateFileA(R"(C:\Users\IEUser\Desktop\BOOTY.TXT)",
                                  FILE_APPEND_DATA,
                                  FILE_SHARE_READ,
                                  nullptr,
                                  OPEN_ALWAYS,
                                  FILE_ATTRIBUTE_NORMAL,
                                  nullptr);

    if (buttfile == INVALID_HANDLE_VALUE) { return -1; }

    if (WriteFile(buttfile, buffer, strlen(buffer), nullptr, nullptr) == 0)
    {
        CloseHandle(buttfile);
        return 1;
    }

    CloseHandle(buttfile);
    return 0;
}
