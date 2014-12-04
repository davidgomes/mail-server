#ifndef SERVER_HPP
#define SERVER_HPP

#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <netinet/in.h>

void server_exit(int exit_value);
void server_setup();
void server_loop();

int socket_descriptor;
int client_socket;
struct sockaddr_in address;
struct sockaddr_in client_address;
socklen_t client_address_size;
int server_port = 9000;

#endif
