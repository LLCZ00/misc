#include <cstdio>
#include <windows.h>

class RuntimeLib
{
private:
    HMODULE LinkedLib;

    void Error(const char* msg)
    {
        printf("Error: %s\n", msg);
        exit(1);
    }

public:
    /* Constructor */
    RuntimeLib(const char* libname) 
    { 
        LinkedLib = GetModuleHandleA(libname);
        if (LinkedLib == NULL)
        {
            LinkedLib = LoadLibraryA(libname);
            if (LinkedLib == NULL) { Error("Failed to load library"); }
        }
    }

    /* Public Function(s) */
    FARPROC LinkFunction(const char* func_name) // Return address of given function
    {
        FARPROC tmplink = GetProcAddress(LinkedLib, func_name);
        if (tmplink == NULL) { Error("Failed to load function"); }
        return tmplink;
    }

    /* Destructor */
    ~RuntimeLib() { if (LinkedLib != NULL) { FreeLibrary(LinkedLib); } }    
};

int main()
{
    auto CheckDebug = (BOOL (CALLBACK *)(void))RuntimeLib("KERNEL32.dll").LinkFunction("IsDebuggerPresent");

    if (!CheckDebug())
    {
        puts("No debugger detected");
    }
    else { exit(2); }

    RuntimeLib mylib = RuntimeLib("TestDLL.dll");
    auto ServiceMain = (void (CALLBACK*)(void))mylib.LinkFunction("ServiceMain");

    ServiceMain();

    return 0;
}