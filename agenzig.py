#-------------------------------------------------------------------------------
# Name:        Agenzig Main Script
# Purpose:     Text-based adventure game engine (i.e. reads actual adventure from config files)
#
# Author:      Thomas Sturges-Allard
#
# Created:     01/11/2011 ish
# Copyright:   (c) Thomas Sturges-Allard 2011
# Licence:      Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#			http://creativecommons.org/licenses/by-nc-sa/3.0/
#-------------------------------------------------------------------------------

import os # For checking for the existence of file and folders
try:
	import configobj #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
except ImportError, e:
	raw_input("ConfigObj module is required. Please install and try again")
	exit(0)
from configobj import *
from time import sleep
from subprocess import Popen
dot = str(os.curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
sep = str(os.sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
#Hopefully the use of these will help make the engine cross-platform
mainfile = dot+sep+"main.agez"
advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
mpc = dot+sep+"mpc-hc.exe"
aplayer = os.access(mpc, os.R_OK)
kpic = dot+sep+"kpic.exe"
gviewer = os.access(kpic, os.R_OK)
if (os.access(advsfolder, os.R_OK)) and (str(os.listdir(advsfolder)) != "[]") :
	if aplayer == True :
		aztheme = dot+sep+"aztheme.aza"
		if os.access(aztheme, os.R_OK) :
			playtheme = Popen([mpc, aztheme])
			sleep(0.5)
	if gviewer == True :
		azsplash = dot+sep+"azsplash.azg"
		if os.access(azsplash, os.R_OK) :		
			viewsplash = Popen([kpic, azsplash])
			sleep(3)
			viewsplash.kill()
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
			choice = raw_input("\nPlease type a number corresponding to the adventure you wish to play >" )
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
	charfolder = advfolder+"Characters"+sep
	print advname+" succesfully loaded\n"		
elif os.access(mainfile, os.R_OK) :
	main = ConfigObj(mainfile, unrepr=True)
	advname = main['Details']['title']
	advfolder = dot+sep
	charfolder = advfolder+"Characters"+sep
else :
	if os.access(advsfolder, os.R_OK) :
		print "The Adventures folder exists but contains no Adventure folders\n"
	else :
		print "No Adventures folder found in script directory\n"
	print "No main file found in script directory\n\nIf you only have/play one Agenzig adventure then it's files\n(main.agez, attributes.agez etc) should be in the same directory as agenzig.py\n\nIf you have/play multiple adventures then the files for each should be kept\nin a subfolder of 'Adventures' which itself should be\nin the same directory as agenzig.py\n"
	raw_input("If you don't know what this means, then you should probably reinstall") #More informative than a crash...
	exit(0)
graphics = advfolder+"Graphics"+sep
if aplayer == True :
	theme = dot+sep+"theme.aza"
	if os.access(theme, os.R_OK) :
		playtheme = Popen([mpc, theme])
		sleep(0.5)
if gviewer == True :
	splash = advfolder+"splash.azg"
	if os.access(splash, os.R_OK) :		
		viewsplash = Popen([kpic, splash])
		sleep(3)
		viewsplash.kill()
done = 0
if not os.path.exists(charfolder):
    os.makedirs(charfolder)
while done == 0 :
	chars = os.listdir(charfolder)
	chars.reverse()
	charsno = len(chars)
	opt = 1
	if charsno != 0 :
		print "Listing characters"
		while charsno != 0 :
			print "%s) %s" %(opt,chars.pop())
			charsno = charsno-1
			opt = opt+1
		print "\n%s) New Character\n" %(opt)
		choice = raw_input("Please type a number corresponding to the above option you require >" )
	else :
		print "No characters found"
		print "Initiating character creation"
		choice = str(1)
	if choice.isdigit() == 1 :
		sel = int(choice)
		if sel == opt :
			from agccreator import createchar
			createchar(advfolder)
		else:
			if sel <= opt :
				chars2 = os.listdir(charfolder)
				charfile = charfolder+sep+str(chars2.pop((sel-1)))
				character = ConfigObj(charfile, unrepr=True)
				charname = 	character['Basics']['charname']
				done = 1
			else:
				print "Value given is not within option range\n"
	else:
		print "Input must be a number"
#Setting main and character varibles for easy access
scene = str(character['Basics']['scene'])
title = main['Details']['title']
subtitle = "an Agenzig adventure"
author = main['Details']['author']
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
health = int(character['Vitals']['1']) #bodge
fatigue = int(character['Vitals']['2'])
strength = int(character['Attributes']['1'])
knowledge = int(character['Attributes']['2'])
dexterity = int(character['Attributes']['3'])
willpower = int(character['Attributes']['4'])
constitution = int(character['Attributes']['5'])
charisma = int(character['Attributes']['6'])
perception = int(character['Attributes']['7'])
equipment = character['Items']['equipment']
inventory = character['Items']['inventory']
# Loading other files
scenefile = advfolder+sep+"scenes.agez"
scenes = ConfigObj(scenefile, unrepr=True)
choicefile = advfolder+sep+"choices.agez"
choices = ConfigObj(choicefile, unrepr=True)
confrontationfile = advfolder+sep+"confrontations.agez"
confrontations = ConfigObj(confrontationfile, unrepr=True)
attributefile = advfolder+sep+"attributes.agez"
attributes = ConfigObj(attributefile, unrepr=True)
vitalfile = advfolder+sep+"vitals.agez"
vitals = ConfigObj(vitalfile, unrepr=True)
itemfile = advfolder+sep+"items.agez"
items = ConfigObj(infile=itemfile, unrepr=True)
equipmentfile = advfolder+sep+"equipment.agez"
equips = ConfigObj(equipmentfile, unrepr=True)
fight = 0

vittotal = vitals['total']
attotal = attributes['total']

if sel!= opt :
	print "Continuing adventure\n"
while 7 != 3 : #Basically, you're not getting out of this loop...
	if	scene in character['Scene States'] :
		scenestate = character['Scene States'][scene]
	else :
		scenestate = str(1)
	print scenes[scene][scenestate]['description']
	scenechoicecodes = scenes[scene][scenestate]['choices']
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
	print "\n"+scenechoices
	sceneb = scene
	scenestateb = scene
	scenechanged = 0
	statusgen = 0
	sstatusgen = 0
	invlistgen = 0
	equiplistgen = 0
	itemused = 0
	from decimal import Decimal
	from math import ceil
	while scenechanged == 0 :
		prompt = raw_input(">") #The main prompt!
		prompt = prompt.lower()
		if prompt == "" :
			pass
		elif (prompt == "choices") or (prompt == "c") :
			print "\n"+scenechoices
		elif (prompt == 'status') or (prompt == "s") :
			if (statusgen != 1) :
				statuslist = "You are:\n"
				statchanged = 0
				vitno = 0
				while vitno != vittotal :
					vitno = vitno+1
					svitno = str(vitno)
					ltbexists = 1
					try:
						vitals[svitno]['Descriptors']['lessthanbase']
					except KeyError, e:
						ltbexists = 0
					mtbexists = 1
					try:
						vitals[svitno]['Descriptors']['morethanbase']
					except KeyError, e:
						mtbexists = 0
					if vitals[svitno]['view'] == 'never' :
						pass
					elif (vitals[svitno]['view'] == 'all') and (vitals[svitno]['maxval'] >= vitals[svitno]['baseval']) and (mtbexists == 1) and (ltbexists == 1) :	
						baserange = ((Decimal(vitals[svitno]['maxval']-vitals[svitno]['baseval'])/vitals[svitno]['Descriptors']['morethanbase']['total'])+(Decimal(vitals[svitno]['baseval']-1)/vitals[svitno]['Descriptors']['lessthanbase']['total']))/2
						basemin = int(round(vitals[svitno]['baseval']-((baserange-1)/2)))
						basemax = int(round(vitals[svitno]['baseval']+((baserange-1)/2)))
						if (character['Vitals'][svitno] >= basemin) and (character['Vitals'][svitno] <= basemax) :
							vitlevel = vitals[svitno]['Descriptors']['base']
						elif character['Vitals'][svitno] < basemin :
							lowdescsec = Decimal(basemin-1)/vitals[svitno]['Descriptors']['lessthanbase']['total']
							descno = str(int(ceil(character['Vitals'][svitno]/lowdescsec)))
							if int(descno) < 1 :
								descno = '1'
							vitlevel = vitals[svitno]['Descriptors']['lessthanbase'][descno]['text']
						elif character['Vitals'][svitno] > basemax :
							highdescsec = Decimal(vitals[svitno]['maxval']-basemax)/vitals[svitno]['Descriptors']['morethanbase']['total']
							descno = str(int(ceil(character['Vitals'][svitno]/highdescsec)))
							if int(descno) < 1 :
								descno = '1'
							vitlevel = vitals[svitno]['Descriptors']['lessthanbase'][descno]['text']
						statuslist = statuslist+vitlevel+"\n"
					elif ((vitals[svitno]['view'] == 'lessthanbase') and (ltbexists == 1)) :
						if character['Vitals'][svitno] < vitals[svitno]['baseval'] :
							lowdescsec = (Decimal(vitals[svitno]['baseval'])-1)/vitals[svitno]['Descriptors']['lessthanbase']['total']
							descno = str(int(ceil(character['Vitals'][svitno]/lowdescsec)))
							if int(descno) < 1 :
								descno = '1'
							vitlevel = vitals[svitno]['Descriptors']['lessthanbase'][descno]['text']
							statuslist = statuslist+vitlevel+"\n"
					else :
						print "vitals.agez is corrupt (vital number %s)" %(svitno)
				statuslist = statuslist+"\n"
				attno = 0
				while attno != attotal :
					attno = attno+1
					sattno = str(attno)
					ltbexists = 1
					try:
						attributes[sattno]['Descriptors']['lessthanbase']
					except KeyError, e:
						ltbexists = 0
					mtbexists = 1
					try:
						attributes[sattno]['Descriptors']['morethanbase']
					except KeyError, e:
						mtbexists = 0
					if attributes[sattno]['view'] == 'never' :
						pass
					elif (attributes[sattno]['view'] == 'notzero') and (attributes[sattno]['maxval'] >= attributes[sattno]['baseval']) and (mtbexists == 1) and (ltbexists == 1) :	
						baserange = ((Decimal(attributes[sattno]['maxval']-attributes[sattno]['baseval'])/attributes[sattno]['Descriptors']['morethanbase']['total'])+(Decimal(attributes[sattno]['baseval']-1)/attributes[sattno]['Descriptors']['lessthanbase']['total']))/2
						basemin = int(round(attributes[sattno]['baseval']-((baserange-1)/2)))
						basemax = int(round(attributes[sattno]['baseval']+((baserange-1)/2)))
						if (character['Attributes'][sattno] >= basemin) and (character['Attributes'][sattno] <= basemax) :
							attlevel = attributes[sattno]['Descriptors']['base']
						elif character['Attributes'][sattno] < basemin :
							lowdescsec = Decimal(basemin-1)/attributes[sattno]['Descriptors']['lessthanbase']['total']
							descno = str(int(ceil(character['Attributes'][sattno]/lowdescsec)))
							if descno < 1 :
								descno = 1
							attlevel = attributes[sattno]['Descriptors']['lessthanbase'][descno]['text']
						elif character['Attributes'][sattno] > basemax :
							highdescsec = Decimal(attributes[sattno]['maxval']-basemax)/attributes[sattno]['Descriptors']['morethanbase']['total']
							descno = str(int(ceil(character['Attributes'][sattno]/highdescsec)))
							if int(descno) < 1 :
								descno = '1'
							attlevel = attributes[sattno]['Descriptors']['lessthanbase'][descno]['text']
						statuslist = statuslist+attlevel+"\n"
					elif ((attributes[sattno]['view'] == 'lessthanbase') and (ltbexists == 1)) :
						if character['Attributes'][sattno] < attributes[sattno]['baseval'] :
							lowdescsec = (Decimal(attributes[sattno]['baseval'])-1)/attributes[sattno]['Descriptors']['lessthanbase']['total']
							descno = str(int(ceil(character['Attributes'][sattno]/lowdescsec)))
							if int(descno) < 1 :
								descno = '1'
							attlevel = attributes[sattno]['Descriptors']['lessthanbase'][descno]['text']
							statuslist = statuslist+attlevel+"\n"
					else :
						print "attributes.agez is corrupt (attribute number %s)" %(sattno)
				statusgen = 1
			print statuslist
		elif (prompt == 'equipment') or (prompt == "e") :
			if (equiplistgen != 1) :
				equiptotal = len(equipment)
				opt = 0
				equipmentlist = "You have equipped:\n"
				tempequipment = list(equipment)
				tempequipment.reverse()
				while equiptotal > 0 :
					aequipno = tempequipment.pop()
					equiptotal = len(tempequipment)
					aequipocc = tempequipment.count(aequipno)+1
					opt = opt+1
					aequipdesc = equips[str(aequipno)]['name']
					equipmentlist = equipmentlist+aequipdesc+"\n"
				if opt == 0 :
					equipmentlist = "You have nothing equipped"
				else :
					tempequipment = list(equipment)
				equiplistgen = 1
			print equipmentlist
		elif (prompt == "inventory") or (prompt == "i") or (prompt.startswith("use ") and  (len(prompt) > 4)) or (prompt.startswith("equip ") and  (len(prompt) > 6)) :
			if prompt.startswith("use ") :
				printinv = 0
			else :
				printinv = 1
			if (invlistgen != 1) :
				itemstotal = len(inventory)
				printeditems = []
				opt = 0
				inventorylist = "You are carrying:\n"
				tempinventory = list(inventory)
				tempinventory.reverse()
				while itemstotal > 0 :
					aitemno = tempinventory.pop()
					itemstotal = len(tempinventory)
					if printeditems.count(aitemno) == 0 :
						aitemocc = tempinventory.count(aitemno)+1
						opt = opt+1
						aitemdesc = items[str(aitemno)]['description']
						if aitemocc == 1 :
							aitem = str(opt)+") "+aitemdesc+"\n"
						else :
							aitem = str(opt)+") "+aitemdesc+" x "+str(aitemocc)+"\n"
						inventorylist = inventorylist+aitem
						printeditems.append(aitemno)
				if opt == 0 :
					inventorylist = "You are not carrying anything of note"
				else :
					tempinventory = list(inventory)
				invlistgen = 1
			if printinv == 1:
				print "\n"+inventorylist
			elif printinv == 0 :
				usecode = prompt.lstrip('u')
				usecode = usecode.lstrip('s')
				usecode = usecode.lstrip('e')
				usecode = usecode.lstrip(' ')
				if choice.isdigit() == 1 :
					usecode = int(usecode)
					if usecode <= opt :
						useditem = str(tempinventory.pop((usecode-1)))
						print items[useditem]['usetext']
						itemused = 1
					else :
						print "You are only carrying "+str(len(inventory))+" types of item"
				else :
					print "USE command must be followed by a number"
		elif (prompt == "help") or (prompt == "h") or (prompt == "man") :
			print "\nCommand List"
			print "'choices': review availible options"
			print "'inventory': view your inventory"
			print "'equipment': view what items you have equipped"
			print "'status': view your health, attributes and equipment"
			print "'about': show information about the adventure you are playing"
			print "'help': view these commands again"
			print "'quit': shut down the game engine"
		elif (prompt == "about") or (prompt == "credits") or (prompt == "a"):
			print "\n"+title+" - "+subtitle+" was made by "+author
			print website
			print "You are currently on scene "+scene
		elif (prompt == "quit") or (prompt == "exit") or (prompt == "x") or (prompt == "leave") :
			print "Are you sure you want to quit?"
			confirm = raw_input(">")				
			if (confirm == "yes") or (confirm == "y") or (confirm == "sure") or (confirm == "please") :
				exit(0)
		else :
			print "Try using an ACTUAL command moron"  #Might change this before release...
		if (scene != sceneb) or (scenestate != scenestateb) :
			scenechanged = 1
		if itemused == 1 :
			invlistgen = 0
			itemused = 0
		statchanged = 0
		if statchanged == 1 :
			statusgen = 0