import http.server
import socketserver

PORT = 8001

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # --- CORRECTION ---
        # We deleted login.html, so now we serve index.html directly
        if self.path == '/':
            self.path = '/index.html'
        # ------------------
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Serving frontend at http://localhost:{PORT}")
print("Go to this address in your browser.")

# Allow reuse of the address to prevent "Address already in use" errors on restart
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True

with httpd:
    httpd.serve_forever()