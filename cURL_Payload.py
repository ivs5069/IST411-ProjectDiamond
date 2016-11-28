import os, json

website = input("Please input what website you want header information from: ")
#website = "https://github.com/"

web_Name = website[website.index('/') + 2: website.index('.'):] 
website_inp = "curl -I " + website + "> " + web_Name + ".curl"

os.system(website_inp)


new_Dict = {}
with open(web_Name + ".curl") as f:
	for line in f:
		if(':' in line):
			new_Dict[line[0:line.index(':'):]] = line[line.index(':') + 2::]

f = open(web_Name + ".json", 'w')
f.write(json.dumps(new_Dict))
f.close()

