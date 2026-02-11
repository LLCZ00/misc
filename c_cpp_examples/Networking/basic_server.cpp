/* *
 * Windows API Tests - basic server
 * */

#include <ws2tcpip.h>
#include <Windows.h>
#include <iostream>
#pragma comment(lib, "ws2_32.lib") // link ws2_32.dll

#define MY_PORT "7894"
#define MY_BUFLEN 1024



int main(int argc, char **argv)
{
    /* Initialize Winsock, quite upon failure */
    WSADATA wsadata;
    if (WSAStartup(MAKEWORD(2,2), &wsadata) != 0) // Loads WS2_32.dll (linked via pragma above)
    {
        std::cout << "WSAStartup failed\n";
        return -1;
    }

    /* Determine values for sockaddr structure */
    struct addrinfo hints = {0}; // Hints is basically what you'd prefer
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    struct addrinfo *result = nullptr; // addrinfo we'll use for socket
    if (getaddrinfo(nullptr, MY_PORT, &hints, &result) != 0)
    {
        std::cout << "getaddrinfo failed\n";
        WSACleanup();
        return -1;
    }

    /* Create socket */
    SOCKET listen_sock = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
    if (listen_sock == INVALID_SOCKET)
    {
        std::cout << "socket failed: " << WSAGetLastError() << "\n";
        WSACleanup();
        return -1;
    }

    /* Bind socket */
    if (bind(listen_sock, result->ai_addr, (int)result->ai_addrlen) == SOCKET_ERROR)
    {
        std::cout << "bind failed: " << WSAGetLastError() << "\n";
        freeaddrinfo(result);
        closesocket(listen_sock);
        WSACleanup();
        return -1;
    }
    freeaddrinfo(result); // result addrinfo struct no longer needed

    /* Listen on socket, and accept the next connection */
    if (listen(listen_sock, SOMAXCONN) == SOCKET_ERROR)
    {
        std::cout << "listen failed: " << WSAGetLastError() << "\n";
        closesocket(listen_sock);
        WSACleanup();
        return -1;
    }
    SOCKET remote_sock = accept(listen_sock, nullptr, nullptr);
    if (remote_sock == INVALID_SOCKET)
    {
        std::cout << "accept failed: " << WSAGetLastError() << "\n";
        closesocket(listen_sock);
        WSACleanup();
        return -1;
    }

    /* Recieve incoming data, send something out, close connection */
    char recv_buffer[MY_BUFLEN];
    int rbytes = recv(remote_sock, recv_buffer, MY_BUFLEN, 0);
    if (rbytes > 0)
    {
        std::cout << "Recieved " << rbytes << " bytes:\n";
        std::cout << recv_buffer << "\n";
    }
    else if (rbytes == SOCKET_ERROR)
    {
        std::cout << "recv failed: " << WSAGetLastError() << "\n";
        closesocket(remote_sock);
        closesocket(listen_sock);
        WSACleanup();
        return -1;
    }

    char send_msg[] = "Tiny baby bitch dad\n";
    int sbytes = send(remote_sock, send_msg, (int)strlen(send_msg), 0);
    if (sbytes == SOCKET_ERROR)
    {
        std::cout << "send failed: " << WSAGetLastError() << "\n";
        closesocket(remote_sock);
        closesocket(listen_sock);
        WSACleanup();
        return -1;
    }
    std::cout << sbytes << " bytes sent\n";


    /* Cleanup sockets, unload ws2_32 dll */
    closesocket(listen_sock);
    WSACleanup();
    std::cout << "\nGraceful exit\n";
    return 0;
}