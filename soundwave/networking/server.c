#include <stdio.h>      /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), bind(), and connect() */
#include <arpa/inet.h>  /* for sockaddr_in and inet_ntoa() */
#include <stdlib.h>     /* for atoi() and exit() */
#include <string.h>     /* for memset() */
#include <unistd.h>     /* for close() */
#include "dotenv.h"

#define MAXPENDING 5    /* Maximum outstanding connection requests */

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(1);
}

float* process(int socket, int size)
{
    float* buffer[size*2];
    int message_size;

    /* Receive message from client */
    if ((message_size = recv(socket, buffer, size*2, 0)) < 0)
        DieWithError("recv() failed");

    /* Send received string and receive again until end of transmission */
    while (message_size > 0)      /* zero indicates end of transmission */
    {
        /* See if there is more data to receive */
        if ((message_size = recv(socket, buffer, size*2, 0)) < 0)
            DieWithError("recv() failed");
    }

    close(socket);
    return buffer;
}

float* receive_message()
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

    /* Create socket for incoming connections */
    if ((server_sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");
      
    /* Construct local address structure */
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);

    /* Bind to the local address */
    if (bind(server_sock, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0)
        DieWithError("bind() failed");

    /* Mark the socket so it will listen for incoming connections */
    if (listen(server_sock, MAXPENDING) < 0)
        DieWithError("listen() failed");

    /* Set the size of the in-out parameter */
    length = sizeof(client_addr);

    /* Wait for a client to connect */
    if ((client_sock= accept(server_sock, (struct sockaddr *) &client_addr, 
                            &length)) < 0)
        DieWithError("accept() failed");

    float* buffer = process(client_sock, size);
    for(int i = 0; i < size; i)
    {
        printf("Received [%f, %f]\n", buffer[i], buffer[i+1]);
        i = i + 2;
    }
}

int main(int argc, char *argv[])
{
    printf("Starting server\n");
    receive_message();
    exit(0);
}
