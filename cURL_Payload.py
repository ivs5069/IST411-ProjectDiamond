import os, json

#Get the website that the user wants to use
website = input("Please input what website you want header information from: ")
#website = "https://github.com/" #Default value for testing so I don't have to keep putting in a website

web_Name = website[website.index('/') + 2: website.index('.'):]  #Get the name of the website

#Create the string for the cURL command.Saves the cURL output to the websites name with file extention .curl"
website_inp = "curl -I " + website + "> " + web_Name + ".curl"

#run the command
os.system(website_inp)

#Create an empty dictionary
new_Dict = {}

#Open the .curl file and iterate through it
with open(web_Name + ".curl") as f:
	for line in f:
		#If the line contains the : character, add it to the dictionary.
		if(':' in line):
			new_Dict[line[0:line.index(':'):]] = line[line.index(':') + 2::]

#Create a new file to hold the json file, write to the file the Json file, and then close the file
f = open(web_Name + ".json", 'w')
f.write(json.dumps(new_Dict))
f.close()

