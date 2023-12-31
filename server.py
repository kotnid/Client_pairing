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
connected = []

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
                client_socket.sendall(func.print_list(connected_clients).encode('utf-8'))
            elif data.startswith("pair"):
                pair_id = data.split(" ")[1]
                if connected_clients[client_id]["pair"] != 0:
                    client_socket.sendall("pair 3".encode('utf-8'))
                else:
                    if pair_id in connected_clients:
                        client_info = connected_clients[client_id]
                        if client_info["pair"] == 0 and pair_id != client_id:
                            connected_clients[client_id]["pair"] = pair_id
                            connected_clients[pair_id]["pair"] = client_id
                            connected_clients[pair_id]["socket"].sendall("pair 0".encode('utf-8'))
                            client_socket.sendall("pair 0".encode('utf-8'))
                        else:
                            client_socket.sendall("pair 2".encode('utf-8'))
                    else:
                        client_socket.sendall("pair 1".encode('utf-8'))
            elif data.startswith("disconnect"):
                pair_id = connected_clients[client_id]["pair"]
                if pair_id != 0:
                    if pair_id in connected_clients:
                            connected_clients[pair_id]["pair"] = 0
                            pair_socket = connected_clients[pair_id]["socket"]
                            pair_socket.sendall("disconnect".encode('utf-8'))

                    connected_clients[client_id]["pair"] = 0
                    client_socket.sendall("dis 0".encode('utf-8'))
                else:
                    client_socket.sendall("dis 1".encode('utf-8'))

        except ConnectionResetError:
            print(f"=== Client {client_address} forcibly closed the connection ===")
            break
        
    # not pair when disconnect    
    pair_id = connected_clients[client_id]["pair"]
    if pair_id != 0:
        if pair_id in connected_clients:
                connected_clients[pair_id]["pair"] = 0
                pair_socket = connected_clients[pair_id]["socket"]
                pair_socket.sendall("disconnect".encode('utf-8'))
    del connected_clients[client_id]
    connected.remove(client_socket)
    client_socket.close()

# Accept new clients
def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        client_id = str(uuid.uuid4())[:6]
        connected.append(client_socket)
        print(f"=== Accepted connection : {client_id} - {client_address} ===")

        
        connected_clients[client_id] = {"addr":client_address,"pair":0,"socket":client_socket}
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
    for client_socket in connected:
        client_socket.close()

    server_socket.close()
    sys.exit(0)


start_server()
signal.signal(signal.SIGINT, terminate_server)

while True:
    pass