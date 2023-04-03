import ipaddress
import socket
import logging
import configparser
import sys
import re
from datetime import time

import clients as clients

#logging.basicConfig(filename='p2p.log', level=logging.DEBUG)

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


config = configparser.ConfigParser()
config.read('config.ini')

listen_host = config.get('SERVER', 'listen_ip')
listen_port = config.getint('SERVER', 'listen_port')
System_name = config.get('SERVER',  'System_Name')
start_ip = config['SCAN']['StartIP']
end_ip = config['SCAN']['EndIP']
start_port = int(config['SCAN']['StartPort'])
end_port = int(config['SCAN']['EndPort'])
scan_interval = int(config['SCAN']['scan_interval'])
ConnectTimeout = config.getfloat('SCAN', 'ConnectTimeout')
ReadTimeout = config.getfloat('SCAN', 'ReadTimeout')


#crlf pattern
#CommandPattern = r"^(.{13})\"(.+)?\"\r\n$"
#CRLF = "\r\n"

#crlf pattern
CommandPattern = r"^(.{13})\"(.+)?\"$"
CRLF = ""


if listen_host == '0.0.0.0':
    listen_host = ''


# networks = []
#
# for i in range(start_ip, end_ip + 1):
#     for j in range(start_port, end_port + 1):
#         network = {'name': f'Network {i}:{j}', 'ip': f'192.168.0.{i}', 'port': j, 'alive': False}
#         networks.append(network)
#
#     while True:
#         for network in networks:
#             name, ip, port, alive = network['name'], network['ip'], network['port'], network['alive']
#
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#                 try:
#                     sock.connect((ip, port))
#                 except ConnectionRefusedError:
#                     if alive:
#                         print(f"{name} is now down.")
#                     network['alive'] = False
#                     continue
#
#                 message = "PING".encode()
#                 sock.sendall(message)
#
#                 sock.settimeout(ConnectTimeout)
#
#                 try:
#                     data = sock.recv(1024)
#                 except socket.timeout:
#                     if alive:
#                         print(f"{name} is not responding.")
#                     network['alive'] = False
#                     continue
#
#                 if data.decode() == "PONG":
#                     if not alive:
#                         print(f"{name} is now up!")
#                     network['alive'] = True
#
#         time.sleep(scan_interval)



#dotazy

CMD_PING = "TRANSLATEPING"
CMD_TRANSLATE = "TRANSLATELOCL"
CMD_SCAN = "TRANSLATESCAN"
#Odpovedi
RCV_PONG = "TRANSLATEPONG"
RCV_SUCESS = "TRANSLATEDSUC"
RCV_ERROR = "TRANSLATEDERR"


#lokalni slovník
local_dict = {"cousin": "bratranec/sestřenice", "rabbit": "králík", "tie": "kravata", "book": "knížka", "car": "auto"}


def translate_local(word):
    """
    Funkce provede překlad zadaného slova pomocí lokálního slovníku svých pěti slov.

      Args:
          word (str): Slovo k přeložení.

      Returns:
          str: Pokud je slovo nalezeno v lokálním slovníku, funkce vrátí přeložený výraz v řetězci formátu
               TRANSLATEDSUC"prelozene slovo". Pokud slovo není nalezeno, funkce vrátí chybovou zprávu
               v řetězci formátu TRANSLATEDERR"chybova hlaska".
    """
    if word in local_dict:
        return f"{RCV_SUCESS}{local_dict[word]}"
    else:
        return f"{RCV_ERROR}Slovo {word} nenalezeno v lokálním slovníku."


def scan_network(word):
    success_scan = False
    translated_word = ""
    for i in range(int(start_ip.split('.')[3]), int(end_ip.split('.')[3]) + 1):
        ip = start_ip.rsplit('.', 1)[0] + '.' + str(i)
        for port in range(start_port, end_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(ConnectTimeout)
                    s.connect((ip, port))
                    s.settimeout(ReadTimeout)
                    s.sendall(f"{CMD_PING}\"{System_name}\"".encode())
                    cmd, peerName = read_peer(s)
                    if cmd == RCV_PONG:
                        logging.debug(f"{ip}:{port}, Peer: \"{peerName}\"")
                        s.sendall(f"{CMD_TRANSLATE}\"{word}\"".encode())
                        translatecmd, result = read_peer(s)
                        if translatecmd == RCV_SUCESS:
                            success_scan = True
                            translated_word = result
                            break



                    else:
                        logging.debug(f"{ip}:{port}, Not P2P Peer")
            except:
                logging.debug(f"{ip}:{port}, chyba spojeni")
                pass

            if success_scan:
                break
        if success_scan:
            break
    return success_scan,translated_word



def handle_input(s, command, argument):

    if command == CMD_PING:
        s.sendall(f"{RCV_PONG}\"{System_name}\"".encode())

    elif command == CMD_TRANSLATE:
        if argument in local_dict:
            s.sendall(f"{RCV_SUCESS}\"{local_dict[argument]}\"".encode())
        else:
            s.sendall(f"{RCV_ERROR}\"Slovo {argument} nenalezeno v lokálním slovníku.\"".encode())

    elif command == CMD_SCAN:
        success_scan,translated_word = scan_network(argument)
        rcv_command = RCV_SUCESS if success_scan else RCV_ERROR
        s.sendall(f"{rcv_command}\"{translated_word}\"".encode())
    else:
        s.sendall(f"{RCV_ERROR}\"Neplatný příkaz: {command}\"".encode())
        return False
    return True

def read_peer(s):

    cmdline = ""
    cmd = None
    param = None
    s.settimeout(ReadTimeout)
    while True:
        try:
            cmdline += s.recv(1024).decode()
            commandMatch = re.search(CommandPattern, cmdline)
            if commandMatch:
                cmd = commandMatch.group(1)
                param = commandMatch.group(2)
                #logging.debug(f"Received cmd: {cmd} with param {param}")
                break

        except socket.timeout:
            logging.debug("Read timed out")
            cmdline = ""
            break
    return cmd, param

def handle_client(client_socket, client_address):
    logging.debug(f"Client Connected: {client_address}")
    #client_socket.send(b"Welcome to the P2P program!\r\n")
    client_socket.settimeout(ReadTimeout)
    # readed = ""
    while True:
        cmd, param = read_peer(client_socket)
        if cmd:
            logging.debug(f"Client: {client_address} Received cmd: {cmd} with param {param}")
            out = handle_input(client_socket, cmd, param)
            logging.debug(f"Client: {client_address} Received cmd: {cmd} with param {param} handled with status {out}")
        else:
            break

        # try:
        #     readed += client_socket.recv(1024).decode()
        #     commandMatch = re.search(CommandPattern, readed)
        #     if commandMatch:
        #         cmd = commandMatch.group(1)
        #         param = commandMatch.group(2)
        #         logging.debug(f"Received cmd: {cmd} with param {param}")
        #         out = handle_input(client_socket, cmd, param)
        #         logging.info(out)
        #         readed = ""
        #
        # except socket.timeout:
        #     logging.debug("Receive timed out")
        #     break
    logging.debug(f"Client Disonnected: {client_address}")
    client_socket.close()

def main():
    # while True:
    #     user_input = input("Zadejte příkaz: ")
    #     if user_input == "exit":
    #         break
    #     print(handle_input(user_input))
    logging.debug(f"Starting P2P program...")


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen()
    logging.debug(f"Listening on address {listen_host} and port {listen_port}")

    #scan_network()


    while True:
        try:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)

        except socket.timeout:
            logging.debug("Connection timed out")
        except KeyboardInterrupt:
            break
        finally:
            client_socket.close()

    # for client_socket in clients:
    #     client_socket.close()

    server_socket.close()
    logging.debug("P2P program stopped")


if __name__ == '__main__':
    main()
