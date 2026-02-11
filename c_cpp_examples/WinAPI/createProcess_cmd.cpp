/* *
 * Windows API Tests - Creating cmd process
 * */

#include <Windows.h>
#include <iostream>

static int spawn_shell()
{
    /* Startup & process info structures for new process */
    STARTUPINFOA sinfo;
    PROCESS_INFORMATION pinfo;
    ZeroMemory(&sinfo, sizeof(sinfo)); // Clear memory locations, to avoid possible errors
    ZeroMemory(&pinfo, sizeof(pinfo));
    sinfo.cb = sizeof(sinfo);


    /* Run cmd.exe (consider obfuscation) */
    char cmdline[] = "cmd.exe";
    if (!CreateProcessA(nullptr,
                        cmdline,
                        nullptr,
                        nullptr,
                        TRUE,
                        0,
                        nullptr,
                        nullptr,
                        &sinfo,
                        &pinfo)
                        ) {return -1;}

    /* Wait for process to complete, then release */
    WaitForSingleObject(pinfo.hProcess, INFINITE);
    CloseHandle(pinfo.hProcess);
    CloseHandle(pinfo.hThread);

    return 0;
}

int main(int argc, char **argv)
{

    spawn_shell();

    std::cout << "\nGraceful exit\n";
    return 0;
}