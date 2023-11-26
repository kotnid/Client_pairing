import socket
import func 
import threading

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


def choose_client():
    client_id = input("Enter the client ID to pair with: ")
    client_socket.sendall(f"pair {client_id}".encode('utf-8'))
   


def disconnect_client():
    client_socket.sendall("disconnect".encode('utf-8'))

def receive_messages():
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data == "connect":
            print("Paired")
        elif data == "disconnect":
            print("Not paired")
        elif data.startswith("pair"):
            code = data.split(" ")[1]
            if code == "0":
                print("Connected")
            elif code == "1":
                print("Client not found")
            elif code == "2":
                print("Client not available")
            elif code == "3":
                print("Connected to other client already")
        elif data.startswith("dis"):
            code = data.split(" ")[1]
            if code == "0":
                print("Disconnected")
            elif code == "1":
                print("Fail to disconnect")
        else:
            print(data)
        
def start_client():
    connect_to_server()
    message_thread = threading.Thread(target=receive_messages)
    message_thread.daemon = True
    message_thread.start()

    while True:
        choice = input("Enter your choice (1: Disconnect, 2: Get Connected Clients, 3: Choose Client): ")

        if choice == "1":
            disconnect_from_server()
            break
        elif choice == "2":
            request_connected_clients()
        elif choice == "3":
            choose_client()
        elif choice == "4":
            disconnect_client()
        else:
            print("Invalid choice. Please try again.")

start_client()