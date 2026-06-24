import http.server
import socketserver
import os
import sys

PORT = 8085
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

Handler = MyHttpRequestHandler

httpd = None
for p in range(PORT, PORT + 50):
    try:
        httpd = socketserver.TCPServer(("", p), Handler)
        PORT = p
        break
    except OSError:
        continue

if httpd is None:
    print("Could not find an open port.")
    sys.exit(1)

print(f"====================================================")
print(f"   CYNOX 4 - LIVE MOCK SERVER RUNNING             ")
print(f"====================================================")
print(f" Serving folder: {DIRECTORY}")
print(f" Click here to view live dashboard: http://localhost:{PORT}/mock_app.html")
print(f" Press CTRL+C to stop the server.")
print(f"====================================================")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server. Goodbye!")
except Exception as e:
    print(f"Error starting server: {e}")
