import socket


def main():
    # The tester will then send an HTTP GET request to your server:

    # $ curl -v http://localhost:4221
    # Your server must respond to the request with the following response:

    # HTTP/1.1 200 OK\r\n\r\n

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket.accept() # wait for client

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)
        print(data)
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        client_socket.close()
        


if __name__ == "__main__":
    main()
