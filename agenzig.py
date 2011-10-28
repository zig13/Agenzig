import os
dot = str(os.curdir)
sep = str(os.sep)
mainfile = dot+sep+"main.agez"
if os.access(mainfile, os.R_OK) :
	main = ConfigObj(mainfile, encoding='UTF8')
	advname = main['Details']['title']
	charfolder = dot+sep+"Characters"+sep
	advfolder = dot+sep
else :
	advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
	done = 0
	while done == 0 :
		advs = os.listdir(advsfolder)
		advs.reverse()
		advsno = len(advs)
		print "Listing adventures"
		opt = 0
		while advsno != 0 :
			opt = opt+1
			print "%s) %s" %(opt,advs.pop())
			advsno = advsno-1
		print ""
		choice = raw_input("Please type a number corresponding to the adventure you wish to play" )
		if choice.isdigit() == 1 :
			sel = int(choice)
			if sel <= opt :
				advs2 = os.listdir(advsfolder)
				advfolder = advsfolder+str(advs2.pop((sel-1)))
				mainfile = advfolder+sep+"main.agez"
				done = 1
			else:
				print "Value given is not within option range"
				print ""
		else:
			print "Input must be a number"
	from configobj import ConfigObj
	main = ConfigObj(mainfile, encoding='UTF8')
	advname = main['Details']['title']
	charfolder = dot+sep+advfolder+sep+"Characters"+sep
	print advname+" succesfully loaded"
	print ""
done = 0
while done == 0 :
	chars = os.listdir(charfolder)
	chars.reverse()
	charsno = len(chars)
	print "Listing characters"
	opt = 1
	while charsno != 0 :
		print "%s) %s" %(opt,chars.pop())
		charsno = charsno-1
		opt = opt+1
	print ""
	print "%s) New Character" %(opt)
	print ""
	choice = raw_input("Please type a number corresponding to the above option you require" )
	if choice.isdigit() == 1 :
		sel = int(choice)
		if sel == opt :
			charname = raw_input("Please enter a charname for your character" )
			charfile = "%s.azc" %(charname)
			done = 1
		else:
			if sel <= opt :
				chars2 = os.listdir(charfolder)
				charfile = str(chars2.pop((sel-1)))
				charname = charfile.rstrip('c')
				charname = charname.rstrip('z')
				charname = charname.rstrip('a')
				charname = charname.rstrip('.')
				done = 1
			else:
				print "Value given is not within option range"
				print ""
	else:
		print "Input must be a number"
charfile = "%s%s.azc" %(charfolder,charname)
character = ConfigObj(charfile, encoding='UTF8')
if sel == opt : #Making a new character
	character['Basics'] = {}
	character['Basics']['charname'] = charname
	character.write()
	print "New character created"