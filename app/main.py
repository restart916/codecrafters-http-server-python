import socket



def root(request, headers):
    return b"HTTP/1.1 200 OK\r\n\r\n"

def echo(request, headers):
    # GET /echo/abc 
    # HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\nabc
    try:
        request_target = request.split(b" ")[1]
        response_body = request_target.split(b"/")[2]
    except:
        response_body = b""
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(response_body)).encode() + b"\r\n\r\n" + response_body

routes = {
    "echo": echo,
    "": root,
}


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)

        request_line = data.split(b"\r\n")[0]
        headers = data.split(b"\r\n")[1:]

        request_target = request_line.split(b" ")[1]
        
        find_route = False
        for route in routes:
            path = request_target.split(b"/")[1].decode()
            if path == route:
                response = routes[route](request_line, headers)
                find_route = True
                break
        
        if not find_route:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.sendall(response)
        
        client_socket.close()


if __name__ == "__main__":
    main()
