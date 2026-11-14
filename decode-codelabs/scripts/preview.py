#!/usr/bin/env python3
"""Serve the generated site, optionally mounted under a project subdirectory."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=8765)
parser.add_argument('--prefix',default='/')
args=parser.parse_args()
prefix='/'+args.prefix.strip('/')+'/' if args.prefix.strip('/') else '/'
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=urlsplit(self.path).path
        if prefix!='/' and not path.startswith(prefix):
            self.send_error(404);return
        self.path='/'+self.path[len(prefix):] if prefix!='/' else self.path
        super().do_GET()
try:
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(ROOT/'site')))
except OSError:
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(ROOT/'site')))
print(f'Local preview: http://127.0.0.1:{server.server_port}{prefix}',flush=True)
print('Keep this command running. Ctrl-C stops only this preview.',flush=True)
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
