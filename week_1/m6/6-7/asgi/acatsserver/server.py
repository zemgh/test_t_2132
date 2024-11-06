import asyncio


class ACatServer:
    def __init__(self, host, port, app):
        self._host = host
        self._port = port
        self._app = app

    async def _handle_client(self, reader, writer):
        try:
            request_data = await reader.read(1024)
            request_text = request_data.decode('utf-8')

            method, path, _ = request_text.split(' ', 2)

            scope = {
                'type': 'http',
                'method': method,
                'path': path,
                'headers': [],
            }

            async def receive():
                return {'type': 'http.request', 'body': b''}


            async def send(message):
                if message['type'] == 'http.response.start':
                    response_lines = self._get_response_lines(message)
                    writer.write(response_lines)

                if message['type'] == 'http.response.body':
                    writer.write(message.get('body', b''))

                await writer.drain()

            await self._app(scope, receive, send)

        except Exception as e:
            print('something wrong with server :(\n', e)

        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass


    def _get_response_lines(self, message) -> bytes:
        status_line = f'HTTP/1.1 {message['status']} OK\r\n'
        print(status_line[:-5])
        headers_list = [f'{key}: {value}\r\n' for key, value in message.get('headers', [])]
        headers_line = ''.join(headers_list)

        return (status_line + headers_line + '\r\n').encode('utf-8')


    async def run(self):
        server = await asyncio.start_server(self._handle_client, self._host, self._port)
        async with server:
            print(f'[ Server started on {self._host}:{self._port} ]')
            await server.serve_forever()

