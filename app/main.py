# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # server_socket = socket.create_server(("localhost", 4221))

    conn, addr = server_socket.accept()  # wait for client
    with conn:
        print(f"connected by {addr}")
        conn.recv(1024)
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        # while True:
        #     data = conn.recv(1024)
        #     if not data:
        #         break
        #     conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
