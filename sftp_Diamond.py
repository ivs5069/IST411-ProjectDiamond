'''
	sftp_Diamond.py
	Author: Ion Sirotkin
	Class: IST 411
	Project: Diamond
	Purpose: Opens a socket server and listens for incoming messages. Decrypts the SSL message,
		 updates the message information, and logs the message in the mongo database. Then 
		 creates a checksum and sends the message and checksum through SFTP.

'''

import socket, ssl, json, hashlib, time, pysftp

#Create the socket for the server, set the address and port number, and set max connections to 5
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 41028))
serversocket.listen(5)

cnopts = pysftp.CnOpts()

cnopts.hostkeys = None #Disable host key checking

cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109}



while True:
	try:
		#Listen for any messages sent through the socket
		connection, address = serversocket.accept()
		connection_stream = ssl.wrap_socket(connection, server_side = True, certfile = "server.crt", keyfile = "server.key")
		#Set max length of data to 2048
		data = connection_stream.read(2048)
		#if a message bigger than 0 comes in
		if(data > 0):
			#Parse the message from JSON to dictionary
			message = json.loads(data)
			
			#Update the Message information
			message["Diamond System"] = "SFTP Diamond"
			message["Diamond Time"] = time.time()

			file_name = message["Website Name"] + "_ion.json"

			#Print out to the user that a message was recieved
			print(" [x] Recieved %r JSON header payload" % str(message["Website Name"]))

			#Parse the updates message back to JSON
			unhashed_message = json.dumps(message)

			#Create an empty dictionary to hold the JSON message and checksum
			hashed_message = {}

			#Set the key of message to be the JSON message
			hashed_message["Message"] = unhashed_message
			
			#Set the checksum of the Json message to the MD5 hash of the JSON file
			hashed_message["Checksum"] = hashlib.md5(unhashed_message.encode()).hexdigest()
			
			#Parse the JSON message with the Checksum in JSON
			hashed_json = json.dumps(hashed_message)
			
			#Send the payload over sftp
			with pysftp.Connection(**cinfo) as sftp:
				try:
					f = open(file_name, 'w')
					f.write(hashed_json)
					f.close()
					sftp.cd('/home/ftpuser')
					sftp.put(file_name)
					sftp.close()
				except:
					print "File transfer issue"

	except Exception, err:
		serversocket.close()
		print err
		exit()
