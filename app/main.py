import socket
import sys

def root(request, headers):
    return b"HTTP/1.1 200 OK\r\n\r\n"

def echo(request, headers):
    try:
        request_target = request.split(b" ")[1]
        response_body = request_target.split(b"/")[2]
    except:
        response_body = b""
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(response_body)).encode() + b"\r\n\r\n" + response_body

def user_agent(request, headers):
    for header in headers:
        if header.startswith(b"User-Agent"):
            user_agent = header.split(b": ")[1]
            break
    
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(user_agent)).encode() + b"\r\n\r\n" + user_agent

def files(request, headers):
    try:
        directory = sys.argv[2]
        request_target = request.split(b" ")[1]
        file_path = request_target.split(b"/")[2].decode()
        full_path = f"{directory}{file_path}"
        with open(full_path, "rb") as file:
            response_body = file.read()
    except:
        return b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    return b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: " + str(len(response_body)).encode() + b"\r\n\r\n" + response_body

routes = {
    "echo": echo,
    "user-agent": user_agent,
    "files": files,
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
