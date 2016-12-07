'''
	socket_Diamond.py
	Author: Ion Sirotkin
	Class: IST411
	Project: Diamond
	Purpose: Recieves a JSON payload from RabbitMQ. Decrypt the JSON payload if it is encrypted in AES.
		 Log the JSON information in the Mongo Database. Send the JSON payload to the next Diamond using
		 Socket communications, using a SSL connection.
'''

import json, time, pika, socket, ssl, os
from Crypto.Cipher import AES
from pymongo import MongoClient

#Clear the screen when the server starts up
os.system('clear')

#Define the connection and channel for the RabbitMQ Communication. Set to LocalHost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Declare Queue to 'Diamond'
channel.queue_declare('Diamond')

#Method to run when a message is recieved
def call_Back(channel, method, properties, body):
	
	enc = AES.new('DiamondKey502134', AES.MODE_CBC, 'This is an IV456')
		
	#Convert the JSON file into a dictionary
	
	message = json.loads(enc.decrypt(body))

	#Incriment the amount of times the message went through the Diamond
	message["Diamond Times Looped"] += 1
	
	if(message["Diamond Times Looped"] <= 3):	
		#Update the Message information about what Diamond System it is on and the system time
		message["Diamond System"] = "Socket Diamond"
		message["Diamond Time"] = time.time()

		#Print out that a message has been recieved	
		print(" [x] Recieved %r JSON header payload" % str(message["Website Name"]))

		
		#Send the message over Socket Communications
		json_Message = json.dumps(message)
		
		#Setup the database connection and then add the message to the database
		mongo_client = MongoClient().dbDiamond
		mongo_client.default.insert(message)
		mongo_client.socketDiamond.insert(message)

		#Define the socket client, host, and port
		socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Require cert from server for ssl
		ssl_socket = ssl.wrap_socket(socket_client, ca_certs = "server.crt", cert_reqs = ssl.CERT_REQUIRED)
		

		host = 'localhost'
		port = 41028

		#Connect to the socket and send the payload
		ssl_socket.connect((host,port))
		ssl_socket.write(json_Message)

		ssl_socket.close()

	else:
		print("%r JSON header payload transmission terminated" % str(message["Website Name"]))	
	
	
#Consume data coming in
channel.basic_consume(call_Back, queue = 'Diamond', no_ack = True)

print("RabbitMQ waiting for JSON Payload")

channel.start_consuming()
