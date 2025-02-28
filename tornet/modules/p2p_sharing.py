# modules/p2p_sharing.py
import socket
import threading

def start_p2p_server(port=9002):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] P2P File Sharing Server started on port {port}")

    def handle_client(client_socket):
        file_data = client_socket.recv(1024)
        with open("received_file", "wb") as file:
            file.write(file_data)
        print("[*] File received and saved.")
        client_socket.close()

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_p2p_server()
