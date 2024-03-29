import http.server
import socketserver
from io import BytesIO
import json

PORT = 8000
orders = {}
cc_price = 0
current_epoch = 0
current_epoch_votes = 0
#Handler = http.server.SimpleHTTPRequestHandler

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        #content_length = int(self.headers['Content-Length'])
        #body = self.rfile.read(content_length)
        #cur = str(body)
        #if cur == 'cc_price':
        dict_obj = {}
        dict_obj['cc_price'] = cc_price
        dict_obj['orders'] = orders
        #elif cur == 'orders':
        dict_obj['current_epoch'] = current_epoch
        dict_obj['current_epoch_votes'] = current_epoch_votes
        #elif cur == 'current_epoch':
        b = json.dumps(dict_obj).encode('utf-8')
        print("Current data: \n <<<", dict_obj)
        self.wfile.write(b)

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
        global current_epoch
        global cc_price
        global current_epoch_votes
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
        if "user_id" in cur_j:
            orders[cur_j["user_id"]] = [cur_j["energy"],cur_j["usd"]]
        elif "current_epoch" in cur_j:
            current_epoch = cur_j["current_epoch"]
            current_epoch_votes = 0
        elif "cc_price" in cur_j:
            cc_price = cur_j["cc_price"]
        elif "current_epoch_votes" in cur_j:
            current_epoch_votes += 1

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()



