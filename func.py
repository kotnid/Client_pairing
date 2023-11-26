import socket 

def get_ip():
    hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(hostname)[-1]

    for ip in ip_addresses:
        if ip.startswith("192.168"):
            return str(ip)