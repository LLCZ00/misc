/*
Basic client/server program, for executable tests
- Linux/GCC

References:
https://www.binarytides.com/socket-programming-c-linux-tutorial/
https://people.cs.rutgers.edu/~pxk/rutgers/notes/sockets/
*/
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>    

#define BUFFERSIZE 1024
#define BACKLOG 3


static void delete_exe(char *exe_path)
{
    if (remove(exe_path) != 0)
    {
        puts("Failed to delete executable.");
    }
}

static int validate_number(char *numstring)
{
    while (*numstring)
    {
        if (!isdigit(*numstring))
        {
            return 0; // False
        }
        numstring++;
    }
    return 1; // True
}

int server(char *port)
{
    char *default_msg = "Server connection message.\n";
    char recv_buffer[BUFFERSIZE];
    struct sockaddr_in my_addr;
    struct sockaddr_in client_addr;
    socklen_t addr_size;
    int sock_fd, client_sock;
    int sockoptval = 1;

    memset((char *)&my_addr, 0, sizeof(my_addr));
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(atoi(port));
    my_addr.sin_addr.s_addr = INADDR_ANY;

    if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        puts("Failed to create socket.");
        return 1;
    }
    if (setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &sockoptval, sizeof(int)) < 0)
    {
        puts("Error setting socket options.");
        close(sock_fd);
        return 1;
    }
    if (bind(sock_fd, (struct sockaddr *)&my_addr, sizeof(struct sockaddr_in)) < 0)
    {
        puts("Binding error.");
        close(sock_fd);
        return 1;
    }
    if (listen(sock_fd, BACKLOG) < 0)
    {
        puts("Listening socket error.");
        close(sock_fd);
        return 1;
    }

    printf("Listening on port %s...\n", port);

    memset(recv_buffer, 0, sizeof(recv_buffer));

    if ((client_sock = accept(sock_fd, (struct sockaddr *)&client_addr, &addr_size)) > 0)
    {
        printf("\nConnection from %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
        if (read(client_sock, recv_buffer, BUFFERSIZE))
        {
            printf("Data recieved: %s\n", recv_buffer);
        }
        if (write(client_sock, default_msg, strlen(default_msg)))
        {
            puts("Data sent.");
        }        
        close(client_sock);
        puts("Connection closed.");
    }

    close(sock_fd);
    puts("\nServer closed.");
    return 0;
}

int client(char *ip_address, char *port)
{
    char *default_msg = "Client connection message.\n";
    char recv_buffer[BUFFERSIZE];
    struct sockaddr_in server_addr;
    int sock_fd;

    memset((char *)&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(atoi(port));
    server_addr.sin_addr.s_addr = inet_addr(ip_address);

    if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        puts("Failed to create socket.");
        return 1;
    }

    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0)
    {
        printf("Failed to connect to %s:%s\n", ip_address, port);
        return 1;
    }

    memset(recv_buffer, 0, sizeof(recv_buffer));

    printf("TCP connection established with %s:%d\n", inet_ntoa(server_addr.sin_addr), ntohs(server_addr.sin_port));
    if (write(sock_fd, default_msg, strlen(default_msg)))
    {
        puts("Data sent.");
    }
    if (read(sock_fd, recv_buffer, BUFFERSIZE))
    {
        printf("Data recieved: %s", recv_buffer);
    }

    close(sock_fd);
    puts("Connection closed.");
    return 0;
}


int main(int argc, char **argv)
{
    
    if (argc != 3)
    {
        printf("Usage:\n(Server) %s -l LOCAL_PORT\n", argv[0]);
        printf("(Client) %s REMOTE_IP REMOTE_PORT\n", argv[0]);
        return 1;
    }

    int index = 1;

    if ((strncmp(argv[index], "-l\0", 3) == 0) || (strncmp(argv[index], "--listen\0", 9) == 0))
    {
        if (!validate_number(argv[index+1]))
        {
            puts("Invalid port number.");
            return 1;
        }
        delete_exe(argv[0]);
        return server(argv[index+1]);
    }
    else 
    {
        if (!validate_number(argv[index+1]))
        {
            puts("Invalid port number.");
            return 1;
        }
        delete_exe(argv[0]);
        return client(argv[index], argv[index+1]);
    }
}

