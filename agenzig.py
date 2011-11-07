#-------------------------------------------------------------------------------
# Name:        Agenzig Main Script
# Purpose:
#
# Author:      Thomas Sturges-Allard
#
# Created:     01/11/2011 ish
# Copyright:   (c) Thomas 2011
# Licence:      Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#			http://creativecommons.org/licenses/by-nc-sa/3.0/
#-------------------------------------------------------------------------------

import os # For checking for the existence of file and folders
try:
	import configobj
except ImportError, e:
	raw_input("ConfigObj module is required. Please install and try again")
	exit(0)
dot = str(os.curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
sep = str(os.sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
mainfile = dot+sep+"main.agez"
advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
if os.access(mainfile, os.R_OK) :
	main = ConfigObj(mainfile, encoding='UTF8')
	advname = main['Details']['title']
	charfolder = dot+sep+"Characters"+sep
	advfolder = dot+sep
elif os.access(advsfolder, os.R_OK):
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
			print ""
			choice = raw_input("Please type a number corresponding to the adventure you wish to play" )
		else :
			choice = raw_input("")
		repeat = 1
		if choice == "" :
			print ""
		elif choice.isdigit() == 1 :
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
			print ""
	from configobj import ConfigObj
	main = ConfigObj(mainfile, encoding='UTF8',list_values=True)
	advname = main['Details']['title']
	charfolder = dot+sep+advfolder+sep+"Characters"+sep
	print advname+" succesfully loaded"
	print ""
else :
	print "Adventures folder missing and no main file found"
	raw_input("If you don't know what this means, then you should probably reinstall")
	exit(0)
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
character = ConfigObj(charfile, encoding='UTF8',list_values=True)
if sel == opt : #Making a new character
	csetup = main['Character Setup']
	character['Basics'] = {}
	character['Basics']['charname'] = charname
	character['Basics']['scene'] = csetup['initialscene']
	import random
	#Setting vitals
	character['Vitals'] = {}
	character['Vitals']['health'] = csetup['initialhealth']
	if 'initialfatigue' in csetup.scalars :
		character['Vitals']['fatigue'] = csetup['initialfatigue']
	#Setting attributes
	character['Attributes'] = {}
	character['Attributes']['strength'] = random.randint(int(csetup['minstrength']), int(csetup['maxstrength']))
	character['Attributes']['knowledge'] = random.randint(int(csetup['minknowledge']), int(csetup['maxknowledge']))
	character['Attributes']['dexterity'] = random.randint(int(csetup['mindexterity']), int(csetup['maxdexterity']))
	character['Attributes']['willpower'] = random.randint(int(csetup['minwillpower']), int(csetup['maxwillpower']))
	character['Attributes']['constitution'] = random.randint(int(csetup['minconstitution']), int(csetup['maxconstitution']))
	character['Attributes']['charisma'] = random.randint(int(csetup['mincharisma']), int(csetup['maxcharisma']))
	character['Attributes']['perception'] = random.randint(int(csetup['minperception']), int(csetup['maxperception']))
	character['Attributes']['Initial Values'] = {}
	character['Attributes']['Initial Values']['strength'] = character['Attributes']['strength']
	character['Attributes']['Initial Values']['knowledge'] = character['Attributes']['knowledge']
	character['Attributes']['Initial Values']['dexterity'] = character['Attributes']['dexterity']
	character['Attributes']['Initial Values']['willpower'] = character['Attributes']['willpower']
	character['Attributes']['Initial Values']['constitution'] = character['Attributes']['constitution']
	character['Attributes']['Initial Values']['charisma'] = character['Attributes']['charisma']
	character['Attributes']['Initial Values']['perception'] = character['Attributes']['perception']
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
	character['Items']['armour'] = csetup['initialarmour']
	character['Items']['Mweapon'] = csetup['initialMweapon']
	character['Items']['Rweapon'] = csetup['initialRweapon']
	character['Items']['inventory'] = csetup['initialinventory']
	character['Scene States'] = {}
	character.write()
	print "New character created"
	print ""
#Setting main and character varibles for easy access
scene = character['Basics']['scene']
title = main['Details']['title']
subtitle = "an Agenzig adventure"
author = "by "+main['Details']['author']
website = "For more information, go to "+main['Details']['website']
if 'currencyonename' in main['Details'].scalars :
		currencyonename = main['Details']['currencyonename']
		currencyone = int(character['Currency']['currencyone'])
		if 'currencytwoname' in main['Details'].scalars :
			currencytwoname = main['Details']['currencytwoname']
			currencytwo = int(character['Currency']['currencytwo'])
		if 'currencythreename' in main['Details'].scalars :
			currencythreename = main['Details']['currencythreename']
			currencythree = int(character['Currency']['currencythree'])
health = int(character['Vitals']['health'])
if 'initialfatigue' in main['Character Setup'] :
	fatigue = int(character['Vitals']['fatigue'])
strength = int(character['Attributes']['strength'])
knowledge = int(character['Attributes']['knowledge'])
dexterity = int(character['Attributes']['dexterity'])
willpower = int(character['Attributes']['willpower'])
constitution = int(character['Attributes']['constitution'])
charisma = int(character['Attributes']['charisma'])
perception = int(character['Attributes']['perception'])
armour = int(character['Items']['armour'])
Mweapon = int(character['Items']['Mweapon'])
Rweapon = int(character['Items']['Rweapon'])
inventory  = eval(character['Items']['inventory'])
# Loading other files
scenefile = advfolder+sep+"scenes.agez"
scenes = ConfigObj(scenefile, encoding='UTF8',list_values=True)
choicefile = advfolder+sep+"choices.agez"
choices = ConfigObj(choicefile, encoding='UTF8',list_values=True)
confrontationfile = advfolder+sep+"confrontations.agez"
confrontations = ConfigObj(confrontationfile, encoding='UTF8',list_values=True)
itemfile = advfolder+sep+"items.agez"
items = ConfigObj(itemfile, encoding='UTF8',list_values=True)
armourfile = advfolder+sep+"armour.agez"
armours = ConfigObj(armourfile, encoding='UTF8',list_values=True)
mweaponfile = advfolder+sep+"mweapons.agez"
mweapons = ConfigObj(mweaponfile, encoding='UTF8',list_values=True)
rweaponfile = advfolder+sep+"rweapons.agez"
rweapons = ConfigObj(rweaponfile, encoding='UTF8',list_values=True)
fight = 0
if sel!= opt :
	print "Continuing adventure"
	print ""
while 7 != 3 : #Basically, you're not getting out of this loop...
	if	scene in character['Scene States'] :
		scenestate = character['Scene States'][scene]
	else :
		scenestate = str(1)
	print scenes[scene][scenestate]['description']
	scenechoicecodes = eval(scenes[scene][scenestate]['choices'])
	choicetotal = len(scenechoicecodes) - 1
	choiceno = 0
	while choiceno != choicetotal :
		achoicecode = scenechoicecodes[choiceno]
		schoicecode = str(achoicecode)
		if choices[str(schoicecode)]['hasrequirements'] == str(1) :
			totalreqs = choices[schoicecode]['requirementno']
			totalreqs = int(totalreqs)
			requirementpass = 0
			reqno = 0
			while reqno != totalreqs :
				reqno = reqno + 1
				reqnos = str(reqno)
				if requirementpass == 0 :
					factors = ['perception', 'charisma', 'constitution', 'willpower', 'dexterity', 'knowledge', 'strength', 'fatigue', 'health', 'currencythree', 'currencytwo', 'currencyone']
					factorstotal = len(factors)
					requirementpass = 1
					while factorstotal != 0 :
						factorname = factors.pop()
						factorstotal = len(factors)
						factorreqtype = str(factorname)+"reqtype"
						afactor = eval(str(factorname))
						if (factorname in choices[schoicecode]['Requirements'][reqnos].scalars) and (requirementpass == 1) :
							if factorreqtype in choices[schoicecode]['Requirements'][reqnos].scalars :
								if choices[schoicecode]['Requirements'][reqnos][factorreqtype] == "morethan" :
									if afactor <= int(choices[schoicecode]['Requirements'][reqnos][factorname]) :
										requirementpass = 0
										factorstotal = 0
								elif choices[schoicecode]['Requirements'][reqnos][factorreqtype] == "lessthan" :
									if afactor >= int(choices[schoicecode]['Requirements'][reqnos][factorname]) :
										requirementpass = 0
										factorstotal = 0
								elif choices[schoicecode]['Requirements'][reqnos][factorreqtype] == "exact" :
									if afactor != int(choices[schoicecode]['Requirements'][reqnos][factorname]) :
										requirementpass = 0
										factorstotal = 0
					factors = ['armour', 'Mweapon', 'Rweapon']
					factorstotal = len(factors)
					while factorstotal != 0 :
						factorname = factors.pop()
						factorstotal = len(factors)
						havefactor = "have"+str(factorname)
						afactor = eval(str(factorname))
						if (havefactor in choices[schoicecode]['Requirements'][reqnos].scalars) and (requirementpass == 1) :
							if afactor != int(choices[schoicecode]['Requirements'][reqnos][havefactor]) :
									requirementpass = 0
									factorstotal = 0
					if ('haveitem' in choices[schoicecode]['Requirements'][reqnos].scalars) and (requirementpass == 1) :
						if not choices[schoicecode]['Requirements'][reqnos]['haveitem'] in inventory :
							requirementpass = 0
				else :
					reqnos = totalreqs
		else :
			requirementpass = 1
		choiceno = choiceno + 1
		if requirementpass == 0 :
			scenechoicecodes.remove(achoicecode)
	choicesleft = len(scenechoicecodes)
	opt = 0
	scenechoices = ""
	while choicesleft != 0 :
		opt = opt+1
		schoicecode = str(scenechoicecodes.pop())
		choicesleft = len(scenechoicecodes)
		achoicedesc = choices[schoicecode]['description']
		achoice = str(opt)+") "+achoicedesc+"\n"
		scenechoices = scenechoices+achoice
	print ""
	print scenechoices
	sceneb = scene
	scenestateb = scene
	scenechanged = 0
	statusgen = 0
	invlistgen = 0
	from decimal import *
	while scenechanged == 0 :
		prompt = raw_input("") #The main prompt!
		if prompt == "" :
			print ""
		elif (prompt == "choices") or (prompt == "Choices") or (prompt == "c") or (prompt == "C") :
			print ""
			print scenechoices
		elif  (prompt == "status") or (prompt == "Status") or (prompt == "s") or (prompt == "S") :
			if statusgen != 1 :
				if health > ((int(main['Attribute Categories']['healthy'])/100)*120) :
					stathealth = "You are EXTREMELY Healthy\n"
				elif (health > int(main['Attribute Categories']['healthy'])) and (health <=  ((int(main['Attribute Categories']['healthy']))/100)*120) :
					stathealth = "You are Unnaturally Healthy\n"
				elif (health <= int(main['Attribute Categories']['healthy'])) and (health >= ((int(main['Attribute Categories']['healthy']))/100)*80) :
					stathealth = "You are Healthy\n"
				elif health >= ((int(main['Attribute Categories']['healthy']))/100)*60 :
					stathealth = "You are Hurt\n"
				elif health >= ((int(main['Attribute Categories']['healthy']))/100)*40 :
					stathealth = "You are Injured\n"
				elif health >= ((int(main['Attribute Categories']['healthy']))/100)*20 :
					stathealth = "You are Severely Injured\n"
				elif health > 0 :
					stathealth = "You are Near Death\n"
				else :
					stathealth = "How are you alive?\n"
				if armour != 0 :
					statarmour = "You are wearing "+str(armours[str(armour)]['description'])+"\n"
				else :
					armour = ""
				if Mweapon != 0 :
					statmweapon = mweapons[str(Mweapon)]['description']
					mw = 1
				else :
					mw = 0
				if Rweapon != 0 :
					statrweapon = rweapons[str(Rweapon)]['description']
					rw = 1
				else :
					rw = 0
				if mw == 1 :
					if rw == 1 :
						statweapons = "You are wielding a "+statmweapon+" and a "+statrweapon+"\n"
					else :
						statweapons = "You are wielding a "+statmweapon+"\n"
				elif rw == 1 :
					statweapons = "You are wielding a "+statrweapon+"\n"
				else :
					statweapons = ""
				status = "Current Status:\n"+stathealth+statarmour+statweapons
				statusgen = 1
			print ""
			print status
		elif (prompt == "inventory") or (prompt == "Inventory") or (prompt == "i") or (prompt == "I"):
			if invlistgen != 1 :
				itemstotal = len(inventory)
				opt = 0
				if itemstotal > 0 :
					inventorylist = "You are carrying:\n"+str(opt)+") "+items[str(inventory.pop())]['description']+"\n"
					while itemstotal != 0 :
						opt = opt+1
						aitemno = str(inventory.pop())
						itemstotal = len(inventory)
						aitemdesc = items[aitemno]['description']
						aitem = str(opt)+") "+aitemdesc+"\n"
						inventorylist = inventorylist+aitem
				else :
					inventorylist = "You are not carrying anything of note"
				inventory  = eval(character['Items']['inventory'])
				invlistgen = 1
			print ""
			print inventorylist
		elif (prompt == "help") or (prompt == "Help") or (prompt == "h") or (prompt == "H") :
			print ""
			print "Command List"
			print "'choices': review availible options"
			print "'inventory': view your inventory"
			print "'status': view your health, attributes and equipment"
			print "'help': view these commands again"
		else :
			print "Try using an ACTUAL command moron"
		if (scene != sceneb) or (scenestate != scenestateb) :
			scenechanged = 1