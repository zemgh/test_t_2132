class CatServer:
    def __init__(self, host, port, app):
        self._host = host
        self._port = port
        self._app = app

    def run(self):
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self._host, self._port))
            server_socket.listen()
            print(f'[ Server started on {self._host}:{self._port} ]')

            while True:
                client_socket, address = server_socket.accept()

                with client_socket:
                    request = client_socket.recv(1024).decode('utf-8')

                    def start_response(status, headers):
                        response_line = f'HTTP/1.1 {status}\r\n'
                        response_headers = ''.join([f'{key}: {value}\r\n' for key, value in headers])
                        result = (response_line + response_headers + '\r\n').encode('utf-8')

                        client_socket.sendall(result)

                    environ = self._get_environ(request, client_socket)
                    response_body = self._app(environ, start_response)

                    for data in response_body:
                        client_socket.sendall(data)


    def _get_environ(self, request, connection):
        request_line = request.splitlines()[0]
        print(request_line)
        method, path, _ = request_line.split()

        return {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.url_scheme': 'http',
            'wsgi.input': connection.makefile('rb'),
        }


    def _get_response_lines(self, status, headers):
        status_line = f'HTTP/1.1 {status}\r\n'

        headers_list = [f'{key}: {value}\r\n' for key, value in headers]
        header_lines = ''.join(headers_list)

        return (status_line + header_lines + "\r\n").encode('utf-8')
