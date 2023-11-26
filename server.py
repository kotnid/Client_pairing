import socket
import func
import threading
import sys
import signal
import uuid

# Initialize
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (func.get_ip(), 9999)
connected_clients = {}

# Handle incoming messages
def handle_client(client_socket, client_address,client_id):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                print(f"=== Client {client_address} disconnected ===")
                break

            print(f"=== Received data from {client_address}: {data} ===")

            if data == "get_clients":
                #  client_socket.sendall(str(list(connected_clients.values())).encode('utf-8'))
                client_socket.sendall(func.print_list(connected_clients).encode('utf-8'))


        except ConnectionResetError:
            print(f"=== Client {client_address} forcibly closed the connection ===")
            break

    del connected_clients[client_id]
    client_socket.close()

# Accept new clients
def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        client_id = str(uuid.uuid4())[:6]
        print(f"=== Accepted connection : {client_id} - {client_address} ===")

        
        connected_clients[client_id] = {"addr":client_address,"pair":0}
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address,client_id))
        client_thread.start()

def start_server():
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("=== Server started running ===")

    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()

# terminate program by ctr+c
def terminate_server(signal, frame):
    print("\n=== Terminating the server ===")
    server_socket.close()
    sys.exit(0)


start_server()
signal.signal(signal.SIGINT, terminate_server)

while True:
    pass