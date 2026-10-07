from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from parser import parse_cv

class NLPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/parse':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                body = json.loads(post_data.decode('utf-8'))
                text = body.get('text', '')
                
                if not text or not text.strip():
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"detail": "Empty text provided"}).encode('utf-8'))
                    return
                
                parsed_data = parse_cv(text)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(parsed_data).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, NLPRequestHandler)
    print('Starting NLP service on port 8000...')
    httpd.serve_forever()
