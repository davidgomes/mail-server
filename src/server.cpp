#include "server.hpp"

void server_exit(int exit_value) {
  close(socket_descriptor);
  close(client_socket);
  exit(exit_value);
}

void server_setup() {
  bzero((void*) &address, sizeof(address));
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = htonl(INADDR_ANY);
  address.sin_port = htons(server_port);
  
  socket_descriptor = socket(AF_INET, SOCK_STREAM, 0);

  if (socket_descriptor < 0) {
    fprintf(stderr, "An error ocurred in socket().\n");
    server_exit(1);
  }

  if (bind(socket_descriptor, (struct sockaddr*) &address, sizeof(address)) < 0) {
    fprintf(stderr, "An error occured in bind().\n");
    server_exit(1);
  }

  if (listen(socket_descriptor, 5) < 0) {
    fprintf(stderr, "An error occuredd in listen().\n");
    server_exit(1);    
  }
}

void server_loop() {
  while (true) {
    client_address_size = sizeof(client_address);
    client_socket = accept(socket_descriptor, (struct sockaddr*) &client_address,
                           &client_address_size);

    if (client_socket > 0) {
      printf("Connection occured.\n");
      close(client_socket);
    }
  }
}

int main() {
  server_setup();
  server_loop();

  close(socket_descriptor);
  close(client_socket);
  
  return 0;
}
