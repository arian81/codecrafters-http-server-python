# Uncomment this to pass the first stage
import socket
import os


def parse(req: bytes):
    processed = str(req).split("\r\n")
    path = processed[0].split(" ")[1]
    if "echo" in path:
        random_string = path[6:]
        resp = f"""HTTP/1.1 200 OK
    Content-Type: text/plain
    Content-Length: {len(random_string)}

{random_string}"""
        return resp.encode("utf-8")
    else:
        return b"HTTP/1.1 404 Not Found\r\n\r\n"


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    if os.name == "nt":
        server_socket = socket.create_server(("localhost", 4221))
    else:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    conn, addr = server_socket.accept()  # wait for client
    with conn:
        print(f"connected by {addr}")
        data = conn.recv(1024)
        conn.sendall(parse(data))
        # while True:
        #     data = conn.recv(1024)
        #     if not data:
        #         break
        #     conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
