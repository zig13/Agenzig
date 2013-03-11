def createchar(path) :
	charname = raw_input("Please enter a name for your character >" )
	success = [charname]
	from configobj import ConfigObj
	charfile = path.charfolder+charname+".azc"
	character = ConfigObj(charfile, unrepr=True)
	main = ConfigObj(path.main, unrepr=True)
	character['Basics'] = {}
	character['Basics']['charname'] = charname
	catlist = main['Categories'].keys() #.agez files are read like dictionaries. This line grabs the keys (in this case the subsections that represent categories) from the chosen section
	character['Categories'] = {}
	for catno in catlist : #Do code below for every category in list
		print "Please select your character's %s from the options below:" % (main['Categories'][catno]['catname'])
		totalvals = len(main['Categories'][catno].keys())-1 #Unfortunately I cannot use the same technique for category values as 'catname' is a key. Instead the keys are counted and one is taken from them and I use a while loop
		valno = 0
		while valno < totalvals :
			valno += 1 #Increments value by 1
			svalno = str(valno)
			print svalno+") "+main['Categories'][catno][svalno]['valname']
		valchoice = raw_input(">")
		while (valchoice.isdigit()) == False or (int(valchoice) > totalvals) or (valchoice == "0"):
			if valchoice.isdigit() == False :
				print "Please enter a number that coresponds to a listed option"
			elif (int(valchoice) > totalvals) or (valchoice == "0") :
				print "Number given is not in range of options"
			valchoice = raw_input(">")
		character['Categories'][catno] = {}
		character['Categories'][catno]['catname'] = main['Categories'][catno]['catname']
		character['Categories'][catno]['valcode'] = int(valchoice)
		character['Categories'][catno]['valname'] = main['Categories'][catno][valchoice]['valname']
	csetup = main['Character Setup']
	character['Basics']['scene'] = str(csetup['initialscene'])
	#Setting vitals
	character['Vitals'] = {}
	character['Vitals']['Initial Values'] = {}
	charvits = csetup['Vitals'].keys()
	for charvitno in charvits :
		character['Vitals'][charvitno] = csetup['Vitals'][charvitno]['val']
		character['Vitals']['Initial Values'][charvitno] = character['Vitals'][charvitno]
	#Setting Attributes
	from random import randint
	character['Attributes'] = {}
	character['Attributes']['Initial Values'] = {}
	charatts = csetup['Attributes'].keys()
	for charattno in charatts :
		character['Attributes'][charattno] = randint(int(csetup['Attributes'][charattno]['minval']), int(csetup['Attributes'][charattno]['maxval']))
		character['Attributes']['Initial Values'][charattno] = character['Attributes'][charattno]
	#Setting Inventory & Equipment
	character['Items'] = {}
	character['Items']['inventory'] = csetup['Inventory']['val']
	character['Items']['Equipment'] = {}
	charequips = csetup['Equipment'].keys()
	for charequipno in charequips :
		character['Items']['Equipment'][charequipno] = csetup['Equipment'][charequipno]['id']
	#Setting currencies
	character['Currency'] = {}
	currencytypes = main['Currencies'].keys()
	for currencyno in currencytypes :
		if currencyno in csetup['Currencies'].keys() :
			character['Currency'][currencyno] = csetup['Currencies'][currencyno]['val']
		else :
			character['Currency'][currencyno] = 0
	character['Scene States'] = {}
	character.write()
	success.append(True)
	return success