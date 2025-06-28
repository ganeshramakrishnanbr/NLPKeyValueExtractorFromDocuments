"""
Super minimal HTTP server with no dependencies except standard Python libraries
"""
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello from minimal Python HTTP server!')
        
    def log_message(self, format, *args):
        print(f"Request: {args[0]} - {args[1]} - {args[2]}")

print("Starting minimal HTTP server on http://127.0.0.1:6789")
server = HTTPServer(('127.0.0.1', 6789), SimpleHandler)
server.serve_forever()
