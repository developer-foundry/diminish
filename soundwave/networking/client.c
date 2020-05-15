#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "dotenv.h"

int sock;
struct sockaddr_in serv_addr;
unsigned short port;

void DieWithError(char *errorMessage)
{
    perror(errorMessage);
    exit(1);
}

void setup_connection()
{
    char *server_ip = getenv("SERVER");
    char *server_port = getenv("PORT");

    port = atoi(server_port);

    if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
        DieWithError("socket() failed");

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family      = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(server_ip);
    serv_addr.sin_port        = htons(port);

    if (connect(sock, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
        DieWithError("connect() failed");
}

void send_data(double* input)
{
    unsigned int length;
    char *step_size = getenv("STEP_SIZE");
    length = atoi(step_size);

    int size = length*2*sizeof(double);
    if (send(sock, input, size, 0) != size)
        DieWithError("send() sent a different number of bytes than expected");
}

void shutdown_connection()
{
    close(sock);
}

int main() {
  env_load("soundwave/.env", false);
  char *step_size = getenv("STEP_SIZE");
  size_t length = atoi(step_size);
  double* input = malloc (length * 2 * sizeof(double));
  FILE* input_file = fopen("data/input-smaller.csv", "r");

  for (size_t count = 0; count < length*2;)
  {
      int got = fscanf(input_file, "%lf,%lf", &input[count], &input[count+1]);
      if (got != 2) break;
      count +=2;
  }

  fclose(input_file);
  setup_connection();
  send_data(input);
  shutdown_connection();
  exit(0);
}
