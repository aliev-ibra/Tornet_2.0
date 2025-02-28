# modules/hidden_chat.py
import socket
import threading

def start_chat_server(port=9001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Listening on port {port}")

    clients = []

    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"[*] Received: {message}")
                for c in clients:
                    if c != client_socket:
                        c.send(message.encode('utf-8'))
            except:
                break
        clients.remove(client_socket)
        client_socket.close()

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_chat_server()
