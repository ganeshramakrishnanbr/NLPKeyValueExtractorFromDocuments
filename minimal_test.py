import http.server
import socketserver

def run_minimal_server():
    PORT = 7000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving at http://127.0.0.1:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_minimal_server()
