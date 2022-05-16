import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8001)
server_socket.bind(server_address)
server_socket.listen(1)

while True:
    print('Ожидаем подключения...')
    client_connection, client_address = server_socket.accept()
    print(f'Запрос от {client_address}')
    data = client_connection.recv(1024).decode()
    print(f'{data}')
    client_connection.close()
