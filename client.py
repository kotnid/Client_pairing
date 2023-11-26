import socket
import func 

# init
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (func.get_ip(), 9999)

def connect_to_server():
    client_socket.connect(server_address)
    print("Connected to the server.")

def disconnect_from_server():
    client_socket.close()
    print("Disconnected from the server.")

def request_connected_clients():
    client_socket.sendall("get_clients".encode('utf-8'))
    data = client_socket.recv(1024).decode('utf-8')
    print(data)

def choose_client():
    client_id = input("Enter the client ID to pair with: ")
    client_socket.sendall(f"pair {client_id}".encode('utf-8'))
    data = client_socket.recv(1024).decode('utf-8')
    if data == "0":
        print("Connected")
    elif data == "1":
        print("Client not found")
    elif data == "2":
        print("Client not available")
    elif data == "3":
        print("Connected to other client already")



def start_client():
    connect_to_server()

    while True:
        choice = input("Enter your choice (1: Disconnect, 2: Get Connected Clients, 3: Choose Client): ")

        if choice == "1":
            disconnect_from_server()
            break
        elif choice == "2":
            request_connected_clients()
        elif choice == "3":
            choose_client()
        else:
            print("Invalid choice. Please try again.")

start_client()