import logging
import socket as st
from argparse import ArgumentParser
from logging import info, warning, debug
from marshal import loads

from termcolor import colored, cprint

logging.basicConfig(filename='client.log', filemode='w', level=logging.INFO,
                    format='[%(asctime)s]%(levelname)s:%(message)s', datefmt='%Y/%m/%d %H:%M:%S')

parser = ArgumentParser('client', 'P2PFileTransfer-client', 'P2P file transfer client')
parser.add_argument('ip', type=str, default='', help='Server IP address')
parser.add_argument('port', type=int, help='Server port')
args = parser.parse_args()

client = st.socket(st.AF_INET6, st.SOCK_STREAM)
client.setblocking(True)
client.connect((args.ip, args.port))
information = loads(client.recv(1024))
if information['info'] == 'start':
    print(f'Filename:{information["filename"]}；\nFile size:{information["size"]}')
    client.sendall('yes'.encode('utf-8'))
    debug('The message was send')
    debug('Server reply:' + client.recv(1024).decode('utf-8'))
    DIR = input(colored('Save directory:', 'yellow')) + '\\'
    with open(DIR + information['filename'], 'wb') as fd:
        while True:
            debug('Waiting for the data...')
            fd.write(client.recv(4096))
            rate = fd.tell() / information['size']
            print(
                colored(f'{rate * 100:.2f}%', 'blue'),
                f'[{colored(round(rate * 50) * "=","green"):-<50}]',
                f'{fd.tell()}{colored("B", "yellow")} / {information['size']}{colored("B", "yellow")}',
                end='\r')
            if fd.tell() >= information['size']: break
    info('Receive complete.')
    cprint('\nReceive complete.'.center(50,'*'), 'green')
else:
    client.close()
    warning('message is not right.')
