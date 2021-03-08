#!/usr/bin/env python3
import http.server
import socketserver


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"yea2")


if __name__ == "__main__":
    with socketserver.TCPServer(('', 8080), Handler) as httpd:
        httpd.serve_forever()