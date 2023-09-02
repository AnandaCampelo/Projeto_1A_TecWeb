import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index, delete, edit, update

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    route = extract_route(request)

    filepath = CUR_DIR / route
    print(str(filepath))
    if filepath.is_file():
        if filepath.suffix == '.css':
            response = build_response(headers='Content-Type: text/css; charset=utf-8') + read_file(filepath) 
        else:   
            response = build_response() + read_file(filepath)
    elif 'delete' in str(filepath):
        print(str(filepath))
        response = delete(request)
    elif 'edit' in str(filepath):
        response = edit(request)
    elif 'update' in str(filepath):
        response = update(request)
    elif route == '':
        response = index(request)

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()
