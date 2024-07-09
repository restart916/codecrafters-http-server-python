import socket
import sys

def root(request, headers, request_body, response_info):
    response_info['status'] = "200 OK"
    return response_info

def echo(request, headers, request_body, response_info):
    try:
        request_target = request.split(b" ")[1]
        response_body = request_target.split(b"/")[2]
    except:
        response_body = b""

    response_info['status'] = "200 OK"
    response_info['headers']['Content-Type'] = "text/plain"
    response_info['headers']['Content-Length'] = str(len(response_body))
    response_info['body'] = response_body
    return response_info

def user_agent(request, headers, request_body, response_info):
    for header in headers:
        if header.startswith(b"User-Agent"):
            user_agent = header.split(b": ")[1]
            break
    
    response_info['status'] = "200 OK"
    response_info['headers']['Content-Type'] = "text/plain"
    response_info['headers']['Content-Length'] = str(len(user_agent))
    response_info['body'] = user_agent
    return response_info

def files(request, headers, request_body, response_info):
    try:
        directory = sys.argv[2]
        request_target = request.split(b" ")[1]
        file_path = request_target.split(b"/")[2].decode()
        full_path = f"{directory}{file_path}"
        with open(full_path, "rb") as file:
            response_body = file.read()
    except:
        return dict(
            http_version="HTTP/1.1",
            headers={},
            status="404 Not Found",
            body=b""
        )

    response_info['status'] = "200 OK"
    response_info['headers']['Content-Type'] = "application/octet-stream"
    response_info['headers']['Content-Length'] = str(len(response_body))
    response_info['body'] = response_body
    return response_info

def create_files(request, headers, request_body, response_info):
    try:
        directory = sys.argv[2]
        request_target = request.split(b" ")[1]
        file_path = request_target.split(b"/")[2].decode()
        full_path = f"{directory}{file_path}"
        with open(full_path, "wb") as file:
            file.write(request_body)
    except:
        response_info['status'] = "404 Not Found"
        return response_info

    response_info['status'] = "201 Created"
    return response_info    

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
        
        response_info = dict(
            http_version="HTTP/1.1",
            headers={},
            status="404 Not Found",
            body=b""
        )

        for header in headers:
            if header.startswith(b"Accept-Encoding"):
                accept_encoding = header.split(b": ")[1].split(b", ")
                if b"gzip" in accept_encoding:
                    response_info['headers']["Content-Encoding"] = "gzip"
                
        find_route = False
        for route_info in routes:
            route = route_info["route"]
            method = route_info["method"]
            if path == route and http_method == method:
                func = route_info["func"]
                response_info = func(request_line, headers, request_body, response_info)
                find_route = True
                break
        
        if not find_route:
            response_info['status'] = "404 Not Found"

        response = f"{response_info['http_version']} {response_info['status']}\r\n"
        for key, value in response_info['headers'].items():
            response += f"{key}: {value}\r\n"
        response += f"\r\n{response_info['body'].decode()}"
        client_socket.sendall(response.encode())
        
        client_socket.close()


if __name__ == "__main__":
    main()
