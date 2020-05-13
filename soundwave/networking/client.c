#include <stdio.h>      /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), connect(), send(), and recv() */
#include <arpa/inet.h>  /* for sockaddr_in and inet_addr() */
#include <stdlib.h>     /* for atoi() and exit() */
#include <string.h>     /* for memset() */
#include <unistd.h>     /* for close() */
#include "dotenv.h"

#define RCVBUFSIZE 32   /* Size of receive buffer */

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(1);
}

void send_data(float* input)
{
    env_load("../.env", false);
    char *server_ip = getenv("SERVER");
    char *server_port = getenv("PORT");
    char *step_size = getenv("STEP_SIZE");

    int sock;
    struct sockaddr_in serv_addr;
    unsigned short port;
    unsigned int length;

    char echoBuffer[RCVBUFSIZE];     /* Buffer for echo string */
    int bytes_rcved, total_bytes_rcved;

    port = atoi(server_port);
    length = atoi(step_size);


    /* Create a reliable, stream socket using TCP */
    if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");

    /* Construct the server address structure */
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family      = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(server_ip);
    serv_addr.sin_port        = htons(port);

    /* Establish the connection to the echo server */
    if (connect(sock, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
        DieWithError("connect() failed");

    /* Send the string to the server */
    if (send(sock, input, length, 0) != length)
        DieWithError("send() sent a different number of bytes than expected");

    close(sock);
}

int main() {
  FILE* input_file = fopen("data/input-smaller.csv", "r");
  size_t length = 1024;
  double* input = malloc (length * 2 * sizeof(double));

  for (size_t count = 0; count < length*2;) {
      int got = fscanf(input_file, "%lf,%lf", &input[count], &input[count+1]);
      if (got != 2) break;
      count +=2;
  }
  fclose(input_file);
  send_data(input);
  free(input);
  exit(0);
}
