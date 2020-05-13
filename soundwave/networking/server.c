#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "dotenv.h"

#define MAXPENDING 5

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(1);
}

double* process(int socket, int size)
{
    double* buffer = malloc (size * 2 * sizeof(double));
    int message_size;
    int total_received = 0;

    while ((total_received < size*2*sizeof(double)))
    {
        if ((message_size = recv(socket, (void*)buffer+total_received, (size*2*sizeof(double)), 0)) < 0)
            DieWithError("recv() failed");
        if (message_size == 0)
            break;

        total_received += message_size;
    }

    return buffer;
}

void receive_message()
{
    env_load("../.env", false);
    char *server_port = getenv("PORT");
    char *step_size = getenv("STEP_SIZE");

    int server_sock;
    int client_sock;
    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;
    unsigned short port;
    unsigned int length;
    int size;

    port = atoi(server_port);
    size = atoi(step_size);

    if ((server_sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");
      
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);

    if (bind(server_sock, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0)
        DieWithError("bind() failed");

    if (listen(server_sock, MAXPENDING) < 0)
        DieWithError("listen() failed");

    length = sizeof(client_addr);

    if ((client_sock= accept(server_sock, (struct sockaddr *) &client_addr, 
                            &length)) < 0)
        DieWithError("accept() failed");

    double* buffer = process(client_sock, size);
    close(client_sock);
    close(server_sock);
}

int main(int argc, char *argv[])
{
    printf("Starting server\n");
    receive_message();
    exit(0);
}
