import http.server
import socketserver
from io import BytesIO
import json

PORT = 8000
orders = {}
#Handler = http.server.SimpleHTTPRequestHandler

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        b = json.dumps(orders).encode('utf-8')
        response.write(b)
        self.wfile.write(response.getvalue())

    def do_DELETE(self):
        self.send_response(200)
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response = BytesIO()
        response.write(b'This is DELETE request. ')
        response.write(body)
        self.wfile.write(response.getvalue())
        cur_j = json.loads(body)
        print(cur_j)
        if cur_j["user_id"] in orders:
           del orders[cur_j["user_id"]]

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())
        cur_j = json.loads(body)
        print(cur_j)
        orders[cur_j["user_id"]] = [cur_j["usd"],cur_j["energy"]]

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()



