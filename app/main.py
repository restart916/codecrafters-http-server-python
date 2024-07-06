import socket
import sys

def root(request, headers, request_body):
    return b"HTTP/1.1 200 OK\r\n\r\n"

def echo(request, headers, request_body):
    try:
        request_target = request.split(b" ")[1]
        response_body = request_target.split(b"/")[2]
    except:
        response_body = b""
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(response_body)).encode() + b"\r\n\r\n" + response_body

def user_agent(request, headers, request_body):
    for header in headers:
        if header.startswith(b"User-Agent"):
            user_agent = header.split(b": ")[1]
            break
    
    return b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: " + str(len(user_agent)).encode() + b"\r\n\r\n" + user_agent

def files(request, headers, request_body):
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

def create_files(request, headers, request_body):
    try:
        directory = sys.argv[2]
        request_target = request.split(b" ")[1]
        file_path = request_target.split(b"/")[2].decode()
        full_path = f"{directory}{file_path}"
        with open(full_path, "wb") as file:
            file.write(request_body)
    except:
        return b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    return b"HTTP/1.1 201 Created\r\n\r\n"

routes = [
    {
        "method": "GET",
        "route": "echo",
        "func": echo,
    },
    {
        "method": "GET",
        "route": "user-agent",
        "func": user_agent,
    },
    {
        "method": "GET",
        "route": "files",
        "func": files,
    },
    {
        "method": "POST",
        "route": "files",
        "func": create_files,
    },
    {
        "method": "GET",
        "route": "",
        "func": root,
    },
]


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)

        request_line = data.split(b"\r\n")[0]
        headers = data.split(b"\r\n")[1:]

        http_method = request_line.split(b" ")[0].decode()
        request_target = request_line.split(b" ")[1]
        path = request_target.split(b"/")[1].decode()
        request_body = data.split(b"\r\n\r\n")[1]
        
        find_route = False
        for route_info in routes:
            route = route_info["route"]
            method = route_info["method"]
            if path == route and http_method == method:
                func = route_info["func"]
                response = func(request_line, headers, request_body)
                find_route = True
                break
        
        if not find_route:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.sendall(response)
        
        client_socket.close()


if __name__ == "__main__":
    main()
