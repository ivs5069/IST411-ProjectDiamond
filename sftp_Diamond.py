import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 40028))
serversocket.listen(5)

while True:
	connection, address = serversocket.accept()
	buf = connection.recv(1024)
	if len(buf) > 0:
		print buf

