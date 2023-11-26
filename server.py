import socket 
import func 
import threading 

# init
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (func.get_ip(), 9999)
connected_clients = []


# handle income msg
def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                print(f"=== Client {client_address} disconnected ===")
                break

            print(f"=== Received data from {client_address}: {data} ===")

            # if data == "get_clients":


        except ConnectionResetError:
            print(f"=== Client {client_address} forcibly closed the connection ===")
            break

    connected_clients.remove(client_socket)
    client_socket.close()

# accept new client 
def accept_clients():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"=== Accepted connection : {client_address} === ")

        connected_clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def start_server():
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("=== server start running ===")

    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()


start_server()