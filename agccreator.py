#-------------------------------------------------------------------------------
# Name:        Agenzig Character Creator
# Purpose:     Character creator for a the text-based adventure game engine - Agenzig
#
# Author:      Thomas Sturges-Allard
#
# Created:     10/09/2012 (was previously integrated into main script
# Copyright:   (c) Thomas Sturges-Allard 2011
# Licence:      Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#			http://creativecommons.org/licenses/by-nc-sa/3.0/
#-------------------------------------------------------------------------------
def createchar( advfolder ) :
	charname = raw_input("Please enter a name for your character >" )
	from os import curdir, sep
	dot = str(curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
	sep = str(sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
	from configobj import ConfigObj
	charfolder = advfolder+"Characters"+sep
	charfile = charfolder+charname+".azc"
	character = ConfigObj(charfile, unrepr=True)
	mainfile = advfolder+sep+"main.agez"
	main = ConfigObj(mainfile, unrepr=True)
	character['Basics'] = {}
	character['Basics']['charname'] = charname
	catlist = main['Categories'].keys() #.agez files are read like dictionaries. This line grabs the keys (in this case the subsections that represent categories) from the chosen section
	character['Categories'] = {}
	for catno in catlist : #Do code below for every category in list
		print "Please select your character's %s from the options below:" % (main['Categories'][catno]['catname'])
		totalvals = len(main['Categories'][catno].keys())-1 #Unfortunately I cannot use the same technique for category values as 'catname' is a key. Instead the keys are counted and one is taken from them and I use a while loop
		valno = 0
		while valno < totalvals :
			valno += 1 #Increments valno by 1
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
	if csetup['technique'] == 1 : #Will eventually add alternative character creation techniques
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
	elif csetup['technique'] == 2 :
		pass
	character.write()
	print "New character created"
	print ""		
if __name__ == '__main__': #If agccreator is run directly code below is run to determine 'advfolder' which is then fed into the above function
	try:
		import configobj #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
	except ImportError, e:
		err = raw_input("ConfigObj module is required. Please install and try again")
		if err != "Override" :
			exit(0)
	from configobj import *
	from os import curdir, sep, access, listdir, R_OK, name, system
	from time import sleep
	from subprocess import Popen
	from itertools import repeat
	dot = str(curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
	sep = str(sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
	if name == 'posix': #If OS is linux-based
		def clr():
			system('clear') #'Clr' will now execute the windows command 'clear' which clears the terminal in Linux
	elif (name == 'nt') or (name == 'ce') or (name == 'dos') : #If OS is Windows
		def clr():
		   system('cls') #'Clr' will now execute the windows command 'cls' which clears the terminal in Windows
	else :
		def clr():
			print "\n" * 10
	#Hopefully the use of these will help make the engine cross-platform
	advfolder = dot+sep
	mainfile = advfolder+"main.agez"
	advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
	print "Welcome to the Agenzig Character Creator"
	if (access(advsfolder, R_OK)) and (str(listdir(advsfolder)) != "[]") :
		advchosen = 0
		repeat = 0
		while advchosen == 0 :
			advs = listdir(advsfolder)
			advs.reverse()
			advsno = len(advs)
			if repeat == 0 :
				print "Listing adventures"
				opt = 0
				while advsno != 0 :
					opt = opt+1
					print "%s) %s" %(opt,advs.pop())
					advsno = advsno-1
				choice = raw_input("\nPlease type a number corresponding to the adventure you wish to create\na character for >" )
			else :
				choice = raw_input(">")
			repeat = 1
			if choice == "" :
				pass
			elif choice.isdigit() == 1 : #This section basically does the reverse of the above one to determine what adventure the inputted number refers to
				sel = int(choice)
				if sel <= opt :
					advs2 = listdir(advsfolder)
					advfolder = advsfolder+str(advs2.pop((sel-1)))+sep
					mainfile = advfolder+sep+"main.agez"
					if access(mainfile, R_OK) :
						advchosen = 1
					else :
						print "Selected adventure folder does not contain a main file"
				else:
					print "Value given is not within option range\n"
			else:
				print "Input must be a number\n"
		main = ConfigObj(mainfile, unrepr=True)
		advname = main['Details']['title']
		charfolder = dot+sep+advfolder+sep+"Characters"+sep
		print advname+" succesfully loaded\n"
		sleep(2)
		clr()
	elif access(mainfile, R_OK) :
		main = ConfigObj(mainfile, unrepr=True)
		advname = main['Details']['title']
		charfolder = dot+sep+"Characters"+sep
		advfolder = dot+sep
		print "You will be creating a character for the %s adventure\n" %(advname)
	else :
		if access(advsfolder, R_OK) :
			print "The Adventures folder exists but contains no Adventure folders\n"
		else :
			print "No Adventures folder found in script directory\n"
		print "No main file found in script directory\n\nIf you only have/play one Agenzig adventure then it's files\n(main.agez, attributes.agez etc) should be in the same directory as agenzig.py\n\nIf you have/play multiple adventures then the files for each should be kept\nin a subfolder of 'Adventures' which itself should be\nin the same directory as agenzig.py\n"
		raw_input("If you don't know what this means, then you should probably reinstall") #More informative than a crash...
		exit(0)
	createchar(advfolder)