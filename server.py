import http.server
import urllib.parse
import http.client
import json


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif parsed_url.path.startswith('/api'):
            query_params = urllib.parse.parse_qs(parsed_url.query)
            function = query_params.get('function', [''])[0]
            start = query_params.get('start', [''])[0]
            end = query_params.get('end', [''])[0]
            url = f"/api/v2/area/{start}:{end}|{function}"

            try:
                connection = http.client.HTTPSConnection('newton.vercel.app')
                connection.request('GET', url)
                response = connection.getresponse()
                data = response.read().decode('utf-8')
                connection.close()

                result = json.loads(data)['result']
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'result': result}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            super().do_GET()


if __name__ == '__main__':
    port = 8080
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
