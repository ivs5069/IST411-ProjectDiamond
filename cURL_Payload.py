'''
	cURL_Payload.py		
	Author: Ion Sirotkin
	Class: IST 411
	Last Revision Date: 11/29/2016
	Project: Diamond
	Purpose: Recieves a website inputed in by a user. Returns a JSON object of the Header information of the website.
		 If the JSON file is successfully returned, this script will send out the JSON file through RabbitMQ to
		 get to the first Diamond system. Also puts the whole JSON file in the logs in MongoDB

'''

import os, json, time, uuid, pika
from pymongo import MongoClient

def file_Error():
	print("File Error. Make sure you have permissions to write to this folder or have disk space to write to.")
	exit()

#Get the website that the user wants to use
website = raw_input("Please input what website you want header information from: ")
#website = "https://github.com/" #Default value for testing so I don't have to keep putting in a website

#If the url conatains www
if("www" in website):
	web_Name = website[website.index('.') + 1 : website[website.index('.') + 1: :].index('.') + website.index('.') + 1:] #Splice the string between the period after www and before the extension

#If the url contains http or https splice the string between the second '/' character and before the extension
elif("http" in website):
	web_Name = website[website.index('/') + 2: website.index('.'):]  #Get the name of the website

#Else statement, splices from the beginning to before the extension
else:
	print("Please try again and input a website. Do not forget to input 'http://' or 'https://'")
	exit()


#Create the string for the cURL command.Saves the cURL output to the websites name with file extention .curl"
website_inp = "curl -I " + website + "> " + web_Name + "_curl.txt"

#run the command
try:
	os.system(website_inp)
except:
	file_Error()	

#Create an empty dictionary
new_Dict = {}

#Open the .curl file and iterate through it
try:
	with open(web_Name + "_curl.txt") as f:
		for line in f:
			#If the line contains the : character, add it to the dictionary.
			if(':' in line):
				new_Dict[line[0:line.index(':'):]] = line[line.index(':') + 2::]
except:
	file_Error()

#Add the date/time and subsystem diamond information
new_Dict["Website Name"] = web_Name
new_Dict["Diamond Time"] = time.time()
new_Dict["Diamond System"] = "cURL Payload"

#Add a unique ID for the message
new_Dict["Diamond Message UUID"] = uuid.uuid4().hex

#Add a times looped so the message doesn't infinitly go through the system
new_Dict["Diamond Times Looped"] = 0

#Create a new file to hold the json file, write to the file the Json file, and then close the file
try:
	f = open(web_Name + ".json", 'w')
except:
	file_Error

json_Object = json.dumps(new_Dict)
f.write(json_Object)
f.close()

#Set up the database connection and then add the json payload to the database
client = MongoClient().dbDiamond
client.default.insert(json.loads(json_Object))
client.cURL.insert(json.loads(json_Object))

#Send the JSON object to the first diamond using RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue = 'Diamond')

channel.basic_publish(exchange='', routing_key = 'Diamond', body=json_Object)
print("JSON File sent on RabbitMQ")


