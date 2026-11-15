"""Serve only the website's public distribution, using the Python standard library."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os


PUBLIC = Path(__file__).resolve().parent / "dist"
PORT = int(os.environ.get("LABS_SITE_PORT", "8768"))


class PublicHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(403, "Directory listing is disabled")
        return None

    def send_head(self):
        path = unquote(urlsplit(self.path).path)
        parts = Path(path).parts
        target = (PUBLIC / path.lstrip("/")).resolve()
        if any(part.startswith(".") for part in parts) or not target.is_relative_to(PUBLIC):
            self.send_error(403, "Forbidden")
            return None
        return super().send_head()

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    handler = partial(PublicHandler, directory=str(PUBLIC))
    server = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    print(f"labsdotgde.afrika: http://127.0.0.1:{PORT}", flush=True)
    print(f"Public directory: {PUBLIC}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
