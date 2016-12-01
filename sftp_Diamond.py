import socket, ssl

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 41028))
serversocket.listen(5)

while True:
	try:
		connection, address = serversocket.accept()
		connection_stream = ssl.wrap_socket(connection, server_side = True, certfile = "server.crt", keyfile = "server.key")
	
		data = connection_stream.read()
		if(data > 0):
			print(data)
	except:
		serversocket.close()
		exit()
