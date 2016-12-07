'''
	rabbit_Diamong.py
	Author: Ion Sirotkin
	Class: IST 411
	Project: Diamond
	Purpose: Recieve a JSON message in Pyro4, and then send the JSON message
		 over RabbitMQ encrypting the message using AES encryption
'''

import Pyro4, json, time, pika, os
from Crypto.Cipher import AES


#Clear the terminal when the server starts up
os.system('clear')


print('Pyro4 waiting for JSON Payload')
#Class to hold the pyro object
class Warehouse(object):
	def __init__(self):
		pass
	#Method to recieve the message from pyro
	@Pyro4.expose
	def store(self, recieved):
		#Load the message
		message = json.loads(recieved)

		print "[x] Recieved %r JSON header payload" % str(message["Website Name"])

		#Update the message information
		message["Diamond System"] = "Rabbit Diamond"
		message["Diamond Time"] = time.time()

		#Put the message back into json
		json_message = json.dumps(message)

		enc = AES.new('DiamondKey502134', AES.MODE_CBC, 'This is an IV456')
		
		length_message_to16 = 16 - (len(json_message) % 16)
		for i in range(length_message_to16):
			json_message += ' '

		cipher_text = enc.encrypt(json_message)	

		#Send the message over RabbitMQ using queue Diamond
		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()
		channel.queue_declare(queue = 'Diamond')
		channel.basic_publish(exchange='', routing_key = 'Diamond', body = cipher_text)

		#close the connection
		connection.close()

#Establish the Pyro name server
with Pyro4.Daemon() as daemon:
	message_uri = daemon.register(Warehouse())
	Pyro4.locateNS().register("ion.diamond.message", message_uri)

	daemon.requestLoop()
