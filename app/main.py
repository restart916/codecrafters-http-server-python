import socket


def is_exist(request_target):
    print('target', request_target)
    return request_target == b"/"

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)
        # print(data)

        request_line = data.split(b"\r\n")[0]
        headers = data.split(b"\r\n")[1:]

        request_target = request_line.split(b" ")[1]
        if is_exist(request_target) == False:
            client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        else:
            client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        client_socket.close()



if __name__ == "__main__":
    main()
