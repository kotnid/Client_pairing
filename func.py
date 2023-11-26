import socket 

def get_ip():
    hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(hostname)[-1]

    for ip in ip_addresses:
        if ip.startswith("192.168"):
            return str(ip)

def print_list(connected_clients):
    output = ""
    for client_id, client_socket in connected_clients.items():
        output += f"{client_id}: \n Socket: {client_socket['addr']}\n Pair : {client_socket['pair']}\n"
    return output