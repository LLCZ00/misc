// MTests.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include <cstdio>
#include <windows.h>

int main()
{
    HANDLE fileHandle = CreateFileA(R"(C:\Users\IEUser\Desktop\VSProjects\MTests\x64\Release\SneakyProgram.exe)", 
                                GENERIC_READ, 
                                FILE_SHARE_READ, 
                                nullptr, 
                                OPEN_EXISTING, 
                                FILE_ATTRIBUTE_NORMAL, 
                                nullptr);

    if (fileHandle == INVALID_HANDLE_VALUE)
    {
        puts("failed to open file");
        return 1;
    }

    LARGE_INTEGER fileSize;

    if (GetFileSizeEx(fileHandle, &fileSize))
    {
        printf("File size: %llu\n", fileSize.QuadPart);
    }


    CloseHandle(fileHandle);
    return 0;
}
