// MTests.cpp : This file contains the 'main' function. Program execution begins and ends there.
//


#include <cstdio>
#include <fstream>
#include <windows.h>

using namespace std;

char buffer[10240];

int main()
{
    
    ifstream myFile(R"(C:\Users\IEUser\Desktop\VSProjects\MTests\x64\Release\SneakyProgram.exe)", ios::in | ios::binary);

    if (!myFile.read(buffer, 10240))
    {
        puts("You fucked up");
    }
    else
    {
        for (int i = 0; i < 4; i++)
        {
            printf("0x%x\n", (unsigned char)buffer[i]);
        }
    }


    myFile.close();
    return 0;
}