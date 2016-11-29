'''
	cURL_Payload.py		
	Author: Ion Sirotkin
	Class: IST 411
	Last Revision Date: 11/28/2016
	Purpose: Recieves a website inputed in by a user. Returns a JSON object of the Header information of the website

'''

import os, json, time, uuid

def file_Error():
	print("File Error. Make sure you have permissions to write to this folder or have disk space to write to.")
	exit()

#Get the website that the user wants to use
#website = input("Please input what website you want header information from: ")
website = "https://github.com/" #Default value for testing so I don't have to keep putting in a website

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

#Create a new file to hold the json file, write to the file the Json file, and then close the file
try:
	f = open(web_Name + ".json", 'w')
except:
	file_Error

f.write(json.dumps(new_Dict))
f.close()

