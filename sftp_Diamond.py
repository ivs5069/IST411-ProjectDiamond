import socket, ssl, json, hashlib, time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 41028))
serversocket.listen(5)

while True:
	try:
		connection, address = serversocket.accept()
		connection_stream = ssl.wrap_socket(connection, server_side = True, certfile = "server.crt", keyfile = "server.key")
	
		data = connection_stream.read(2048)
		if(data > 0):
			message = json.loads(data)
			message["Diamond System"] = "SFTP Diamond"
			message["Diamond Time"] = time.time()

			print(" [x] Recieved %r JSON header payload" % str(message["Website Name"]))

			unhashed_message = json.dumps(message)

			hashed_message = {}

			hashed_message["Message"] = unhashed_message
			
			hashed_message["Checksum"] = hashlib.md5(unhashed_message.encode()).hexdigest()
			
			hashed_json = json.dumps(hashed_message)


	#except:
		#serversocket.close()
		#exit()

	except Exception, err:
		serversocket.close()
		print err
		exit()
