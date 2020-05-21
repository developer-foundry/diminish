#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "dotenv.h"

#define MAXPENDING 5
int server_sock;
int client_sock;
int size;

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(1);
}

void process(int socket, int size, double* buffer)
{
    int message_size;
    int total_received = 0;

    while ((total_received < size*2*sizeof(double)))
    {
        if ((message_size = recv(socket, (void*)buffer+total_received, (size*2*sizeof(double) - total_received), 0)) < 0)
            DieWithError("recv() failed");
        if (message_size == 0)
            break;

        total_received += message_size;
    }
}

void setup_server()
{
    char *server_port = getenv("PORT");
    char *step_size = getenv("STEP_SIZE");

    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;
    unsigned short port;
    unsigned int length;

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
}

void shutdown_server()
{
    close(client_sock);
    close(server_sock);
}

void freedata(double* input)
{
    free(input);
}

void receive_message(double* buffer_out, size_t rowcount, size_t colcount)
{
    double* buffer = malloc (size * 2 * sizeof(double));
    process(client_sock, size, buffer);

    for(int i = 0; i < rowcount; i++)
    {
        for(int j = 0; j < colcount; j++)
        {
            buffer_out[i*colcount+j] = buffer[i*colcount+j];
        }
    }

    free(buffer);
}

int main(int argc, char *argv[])
{
    env_load("diminish/.env", false);
    char *step_size = getenv("STEP_SIZE");
    int size = atoi(step_size);
    double* buffer = malloc(size * 2 * sizeof(double));
    setup_server();
    receive_message(buffer, size, 2);
    shutdown_server();
    free(buffer);
    exit(0);
}
