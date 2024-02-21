import logging
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from mimetypes import guess_type
from os.path import getsize, basename

logging.basicConfig(filename='server.log', filemode='w', level=logging.INFO,
                    format='[%(asctime)s]%(levelname)s:%(message)s', datefmt='%Y/%m/%d %H:%M:%S')

parser = ArgumentParser('server', 'P2PFileTransfer-server', 'The server of P2P file transfer')
parser.add_argument('port', type=int, help='Server port')
parser.add_argument('file', type=str, help='The file of needing share')
args = parser.parse_args()


class RequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200, 'File Transfer')
        self.send_header('Content-Length', str(getsize(file.name)))
        self.send_header('Content-Type', guess_type(file.name)[0])
        self.send_header('Content-Encoding', guess_type(file.name)[1])
        self.end_headers()
        self.flush_headers()

    def do_GET(self):
        self.send_response(200, 'File Transfer')
        self.send_header('Content-Length', str(getsize(file.name)))
        self.send_header('Content-Type', guess_type(file.name)[0])
        self.send_header('Content-Encoding', guess_type(file.name)[1])
        self.send_header('Content-Disposition', f'attachment;filename={basename(file.name)}')
        self.end_headers()
        self.flush_headers()
        while True:
            data = file.read(262144)
            if not data: break
            self.wfile.write(data)


if __name__ == '__main__':
    file = open(args.file, 'rb')
    with ThreadingHTTPServer(('localhost', args.port), RequestHandler) as httpd:
        httpd.serve_forever()
