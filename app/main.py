# Uncomment this to pass the first stage
import socket
import os


def parse(req: bytes):
    processed = req.split(b"\r\n")
    print(processed[0].split(b" "))
    if processed[0].split(b" ")[1] == "/":
        return b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        print("404 sent ")
        return b"HTTP/1.1 404 Not Found\r\n\r\n"
    print(processed)


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
        parse(data)
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        # while True:
        #     data = conn.recv(1024)
        #     if not data:
        #         break
        #     conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
