import logging
import socket as st
from argparse import ArgumentParser
from logging import info, warning, error, debug
from marshal import dumps
from os import stat
from os.path import basename
from time import sleep

from termcolor import colored, cprint

logging.basicConfig(filename='server.log', filemode='w', level=logging.INFO,
                    format='[%(asctime)s]%(levelname)s:%(message)s', datefmt='%Y/%m/%d %H:%M:%S')

parser = ArgumentParser('server', 'P2PFileTransfer-server', 'The server of P2P file transfer')
parser.add_argument('port', type=int, help='Server port')
parser.add_argument('time', type=int, help='The numbers of the persons of will be connected')
parser.add_argument('file', type=str, help='The file of need share')
args = parser.parse_args()

IP = st.getaddrinfo(st.gethostname(), None, st.AF_INET6)[0][4][0]

server = st.socket(st.AF_INET6, st.SOCK_STREAM)
info('Socket was created.')
server.setblocking(True)
server.bind((IP, args.port))
server.listen(5)
cprint(f'Sharing file:{args.file}；\nIP address:{server.getsockname()[0]}\nPort：{server.getsockname()[1]}', 'blue')
try:
    client, addr = server.accept()
    cprint(f'Client {addr[0]}:{addr[1]} was connected.Sending file basic information...', 'blue')
    information = stat(args.file)
    with open(args.file, 'rb') as fd:
        client.send(dumps(
            {'info': 'start',
             'filename': basename(args.file),
             'size': information.st_size}))
        debug(
            f'The client reply {client.recv(1024).decode("utf-8")} is received, and basic file information is transmitted.')
        client.sendall('ok'.encode('utf-8'))
        for i in '43210':
            sleep(1)
            print(f'Transfer will start...{i}', end='\r')
        while data:
            data = fd.read(1024)
            client.send(data)
            rate = fd.tell() / information.st_size
            print(colored(f'{rate * 100:.2f}%', 'yellow'),
                  f'[{colored(round(rate * 50) *"=","green"):-<50}]',
                  f'{fd.tell()}B / {information.st_size}B',
                  end='\r')
    info('Send finished')
    print('Send finished.')
    client.close()
    print(f'\nClient was close the connect.')
except ConnectionResetError:
    error('\nConnect was reset.')
except KeyboardInterrupt:
    warning('\nThe server is close by user')
finally:
    info('Server was close')
    print('\nServer closed.')
    server.close()
