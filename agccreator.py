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
	from os import curdir
	dot = str(curdir)
	from os import sep
	sep = str(sep)
	from configobj import ConfigObj
	charfolder = advfolder+"Characters"+sep
	charfile = charfolder+charname+".azc"
	character = ConfigObj(charfile, unrepr=True)
	mainfile = advfolder+sep+"main.agez"
	main = ConfigObj(mainfile, unrepr=True)
	character['Basics'] = {}
	character['Basics']['charname'] = charname
	if main['Categories']['totalcategories'] != 0 :
		totalcats = main['Categories']['totalcategories']
		character['Categories'] = {}
		remcats = int(totalcats)
		while remcats != 0 :
			print "Please select your character's "+main['Categories'][str(remcats)]['catname']+" from the options below:"
			totalvals = main['Categories'][str(remcats)]['catvalues']
			remvals = int(totalvals)
			count = 0
			while remvals != 0 :
				count = count + 1
				print str(count)+") "+main['Categories'][str(remcats)][str(remvals)]['valname']
				remvals = remvals-1
			valchoice = raw_input(">")
			character['Categories'][str(remcats)] = {}
			character['Categories'][str(remcats)]['catname'] = main['Categories'][str(remcats)]['catname']
			character['Categories'][str(remcats)]['valcode'] = ((totalvals) + 1) - int(valchoice)
			character['Categories'][str(remcats)]['valname'] = main['Categories'][str(remcats)][str(((totalvals) + 1) - int(valchoice))]['valname']
			remcats = remcats-1
		remcats = int(totalcats)
	csetup = main['Character Setup']
	character['Basics']['scene'] = str(csetup['initialscene'])
	from random import randint
	#Setting vitals
	character['Vitals'] = {}
	character['Vitals']['1'] = csetup['initialhealth'] #bodge
	if 'initialfatigue' in csetup.scalars :
		character['Vitals']['2'] = csetup['initialfatigue'] #bodge
	#Setting bodge attributes
	character['Attributes'] = {}
	character['Attributes']['1'] = randint(int(csetup['minstrength']), int(csetup['maxstrength']))
	character['Attributes']['2'] = randint(int(csetup['minknowledge']), int(csetup['maxknowledge']))
	character['Attributes']['3'] = randint(int(csetup['mindexterity']), int(csetup['maxdexterity']))
	character['Attributes']['4'] = randint(int(csetup['minwillpower']), int(csetup['maxwillpower']))
	character['Attributes']['5'] = randint(int(csetup['minconstitution']), int(csetup['maxconstitution']))
	character['Attributes']['6'] = randint(int(csetup['mincharisma']), int(csetup['maxcharisma']))
	character['Attributes']['7'] = randint(int(csetup['minperception']), int(csetup['maxperception']))
	character['Attributes']['Initial Values'] = {}
	character['Attributes']['Initial Values']['1'] = character['Attributes']['1']
	character['Attributes']['Initial Values']['2'] = character['Attributes']['2']
	character['Attributes']['Initial Values']['3'] = character['Attributes']['3']
	character['Attributes']['Initial Values']['4'] = character['Attributes']['4']
	character['Attributes']['Initial Values']['5'] = character['Attributes']['5']
	character['Attributes']['Initial Values']['6'] = character['Attributes']['6']
	character['Attributes']['Initial Values']['7'] = character['Attributes']['7']
	#Setting currencies
	if 'currencyonename' in main['Details'].scalars :
		character['Currency'] = {}
		character['Currency']['currencyone'] = csetup['initialcurrencyone']
		if 'currencyonename' in main['Details'].scalars :
			character['Currency']['currencytwo'] = csetup['initialcurrencytwo']
		if 'currencyonename' in main['Details'].scalars :
			character['Currency']['currencythree'] = csetup['initialcurrencythree']
	#Setting inventory
	character['Items'] = {}
	character['Items']['equipment'] = csetup['initialequipment']
	character['Items']['inventory'] = csetup['initialinventory']
	character['Scene States'] = {}
	character.write()
	print "New character created"
	print ""		
if __name__ == '__main__':
	try:
		import configobj #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
	except ImportError, e:
		raw_input("ConfigObj module is required. Please install and try again")
		exit(0)
	from configobj import *
	import os
	dot = str(os.curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
	sep = str(os.sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
	mainfile = dot+sep+"main.agez"
	advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
	print "Welcome to the Agenzig Character Creator"
	if (os.access(advsfolder, os.R_OK)) and (str(os.listdir(advsfolder)) != "[]") :
		done = 0
		repeat = 0
		while done == 0 :
			advs = os.listdir(advsfolder)
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
					advs2 = os.listdir(advsfolder)
					advfolder = advsfolder+str(advs2.pop((sel-1)))+sep
					mainfile = advfolder+sep+"main.agez"
					if os.access(mainfile, os.R_OK) :
						done = 1
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
	elif os.access(mainfile, os.R_OK) :
		main = ConfigObj(mainfile, unrepr=True)
		advname = main['Details']['title']
		charfolder = dot+sep+"Characters"+sep
		advfolder = dot+sep
		print "You will be creating a character for the %s adventure\n" %(advname)
	else :
		if os.access(advsfolder, os.R_OK) :
			print "The Adventures folder exists but contains no Adventure folders\n"
		else :
			print "No Adventures folder found in script directory\n"
		print "No main file found in script directory\n\nIf you only have/play one Agenzig adventure then it's files\n(main.agez, attributes.agez etc) should be in the same directory as agenzig.py\n\nIf you have/play multiple adventures then the files for each should be kept\nin a subfolder of 'Adventures' which itself should be\nin the same directory as agenzig.py\n"
		raw_input("If you don't know what this means, then you should probably reinstall") #More informative than a crash...
		exit(0)
	createchar(advfolder)