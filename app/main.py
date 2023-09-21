# Uncomment this to pass the first stage
import socket
import os
import threading
import argparse


def parse(req: bytes, directory):
    processed = req.decode("utf-8").split("\r\n")
    method, path, *_ = processed.pop(0).split(" ")
    reqdict = {}
    body = ""
    for i in processed:
        if ":" in i:
            key, value = i.split(": ")
            reqdict[key] = value
        elif i != "":
            body = i
    if path == "/":
        resp = "HTTP/1.1 200 OK\r\n\r\n"
    elif path == "/user-agent":
        resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(reqdict['User-Agent'])}\r\n\r\n{reqdict['User-Agent']}"
    elif "files" in path:
        filename = path[7:]
        if method == "GET":
            if filename in os.listdir(directory):
                with open(os.path.join(directory, filename), "r") as file:
                    data = file.read()
                resp = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(data)}\r\n\r\n{data}"
            else:
                resp = "HTTP/1.1 404 Not Found\r\n\r\n"
        elif method == "POST":
            with open(os.path.join(directory, filename), "wb") as file:
                file.write(body.encode("utf-8"))
            resp = "HTTP/1.1 200 OK\r\n\r\n"
        else:
            resp = "METHOD NOT SUPPORTED"

    elif "echo" in path:
        random_string = path[6:]
        resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}"
    else:
        resp = "HTTP/1.1 404 Not Found\r\n\r\n"
    return resp.encode("utf-8")


def new_conn(conn: socket, addr, directory):
    print(f"connected by {addr}")
    data = conn.recv(1024)
    conn.sendall(parse(data, directory))
    conn.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    parser = argparse.ArgumentParser(description="input file directory")
    parser.add_argument("--directory", type=str)
    args = parser.parse_args()

    # Uncomment this to pass the first stage
    #
    if os.name == "nt":
        server_socket = socket.create_server(("localhost", 4221))
    else:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    threads = []
    while True:
        conn, addr = server_socket.accept()  # wait for client
        thread = threading.Thread(target=new_conn, args=[conn, addr, args.directory])
        thread.start()
        threads.append(thread)


if __name__ == "__main__":
    main()
