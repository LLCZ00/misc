/* *
 * In-line API Hook
 * */

#include <Windows.h>
#include <iostream>
using namespace std;

typedef int (WINAPI *deftrampoline)(HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType);
LPVOID trampoline_addr;

int __stdcall proxy_function(HWND hWnd, LPCSTR lpText, LPCSTR lpCaption, UINT uType)
{
    cout << "Intercepted messageboxA call\n";
    auto trampoline = (deftrampoline)trampoline_addr; // redefine and call MessageBoxA (trampoline)
    return trampoline(hWnd, "hooked", "lmao", uType);
    // return trampoline(hWnd, lpText, lpCaption, uType); // run normally after proxy function does whatever
}

void hook_msgbox()
{
    DWORD getError;
    /* Get memory address of MessageBoxA */
    HINSTANCE user32 = LoadLibraryA("user32.dll");
    auto function_addr = (LPCVOID)GetProcAddress(user32, "MessageBoxA");

    /* Save the first 5 bytes (stack setup) */
    char saved_bytes[5] = {0};
    if (ReadProcessMemory(GetCurrentProcess(), function_addr, saved_bytes, 5, nullptr) == 0)
    {
        getError = GetLastError();
        cout << "ReadProcessMemory Error: " << getError << "\n";
    }

    /* Get offset between MessageBoxA function and proxy function */
    auto src = (ULONGLONG) function_addr + 5; // the address right after the stack setup
    auto dst = (ULONGLONG) ((LPVOID) &proxy_function); // starting address of proxy function
    auto rel_offset = (ULONGLONG *)(dst-src);

    /* Overwrite the first 5 bytes with a jump to proxy_function */
    char patch[5] = {0};
    memcpy(patch, "\xE9", 1); // jmp rel16, aka jmp near, relative to next instruction
    memcpy(patch + 1, &rel_offset, 4); // relative offset to proxy function

    if (WriteProcessMemory(GetCurrentProcess(), (LPVOID) function_addr, patch, 5, nullptr) == 0)
    {
        getError = GetLastError();
        cout << "WriteProcessMemory Error: " << getError << "\n";
    }

    /* Build the trampoline (Run MessageBoxA normally after proxy function is finished) */
    trampoline_addr = VirtualAlloc(nullptr, 11, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    auto resume_addr = (ULONGLONG *)((ULONGLONG) function_addr+5);
    memcpy((BYTE *) trampoline_addr, &saved_bytes, 5); // stack setup
    memcpy((BYTE *) trampoline_addr+5, "\x68", 1); // push
    memcpy((BYTE *) trampoline_addr+6, &resume_addr, 4);
    memcpy((BYTE *) trampoline_addr+10, "\xc3", 1); // retn

}

//int main()
//{
//    MessageBoxA(nullptr, "a fiiiine message box", "bubba dump", 0L);
//    hook_msgbox();
//    MessageBoxA(nullptr, "another fiiiine message box", "gubba bump", 0L);
//    cout << "Program exited successfully\n";
//    return 0;
//}