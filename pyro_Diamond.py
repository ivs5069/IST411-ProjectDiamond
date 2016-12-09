'''
	pyro_Diamond.py
	Author: Ion Sirotkin
	Class: IST 411
	Project: Diamond
	Purpose: Recieves a message from SFTP, checks the validity of the messaage by comparing the checksum, and then
		 sends the message over Pyro. 
'''

import os, time, json, hashlib, Pyro4, os
from pymongo import MongoClient

#Clear the terminal when the server goes up
os.system('clear')

#Locate the URI of the pyro server
with Pyro4.locateNS() as ns:
	for x,y in ns.list(prefix="ion.diamond").items():
		uri = y
warehouse = Pyro4.Proxy(uri)


print("SFTP waiting for JSON Payload")
#create a message object to hold the Pyro Objects to send
class Message(object):
	def __init__(self, message):
		self.message = message

	#Send the message over pyro
	def send(self):
		warehouse.store(self.message)

while True:
	time.sleep(1)
	#Read the files that are in the SFTP folder
	sftp_message = os.popen('ls ../../ftpuser | grep _ion.json').read()
	#Create a list for the different files in the SFTP folder
	sftp_messages = []

	while True:
		#Break if there are no more messages that were grabbed
		if '\n' not in sftp_message:
			break
		else:
			#add the message to the list, and then remove it from the grabbed message string
			sftp_messages.append(sftp_message[:sftp_message.index('\n'):])
			sftp_message = sftp_message[sftp_message.index('\n') + 1 : :]

	#For each message
	for i in sftp_messages:
		#Open the message
		f = open('../../ftpuser/'+i)
		hashed_message = json.loads(f.read())
		#Remove the message from the SFTP folder so it doesn't get read again
		os.remove('../../ftpuser/' + i)

		#If the message checksum is valid
		if hashed_message["Checksum"] == hashlib.md5(hashed_message["Message"].encode()).hexdigest():
			#Update the message information
			message = json.loads(hashed_message["Message"])
			message["Diamond System"] = "Pyro Diamond"
			message["Diamond Time"] = time.time()
			
			#Print out that a message got recieved	
			print "[x] Recieved %r JSON header payload" % str(message["Website Name"])
		
			json_message = json.dumps(message)	
			#Setup the database connection and then add the message to the database
			try:
				mongo_client = MongoClient().dbDiamond
				mongo_client.default.insert(message)
				mongo_client.pyroClient.insert(message)
				MongoClient().close()

			except:
	                        print 'Mongo error. Check if mongo is running.'


			#Send the message over Pyro
			messageObject = Message(json_message)
			messageObject.send()
		else:
			print("Checksum Error")
