#!/usr/bin/env python3


import argparse
import http.server
import logging
import os
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
        self.path = os.path.relpath(os.path.join(
            os.path.dirname(__file__),
            "..",
            "static",
            "index.html",
        ))
        logging.info("PATH = %s", self.path)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
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
        self.send_header("Content-type", "application/pdf")
        self.end_headers()
        doc = generate_pdf_doc([
            PAGES.get(i)
            for i in range(16)
        ])
        self.wfile.write(doc.tobytes())


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting server on 0.0.0.0:%d", args.port)

    with socketserver.TCPServer(('0.0.0.0', args.port), Handler) as httpd:
        httpd.serve_forever()