#!/usr/bin/env python3
import http.server
import socketserver

from zine import PAGES, generate_pdf_doc


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._do_get_default()
        elif self.path == "/pdf":
            self._do_get_pdf()
        else:
            self._do_get_not_found()
    
    def _do_get_default(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"yea2")
    
    def _do_get_not_found(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"not found")

    def _do_get_pdf(self):
        self.send_response(200)
        self.send_header("Content-type", "application/x-pdf")
        self.end_headers()
        doc = generate_pdf_doc([
            PAGES.get(i)
            for i in range(16)
        ])
        self.wfile.write(doc.tobytes())


if __name__ == "__main__":

    with socketserver.TCPServer(('', 8081), Handler) as httpd:
        httpd.serve_forever()