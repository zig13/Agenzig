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
try:
	import configobj #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
except ImportError, e:
	err = raw_input("ConfigObj module is required. Please install and try again")
	if err != "Override" :
		exit(0)
from configobj import *
from os import curdir, sep, access, listdir, R_OK, makedirs, path, name, system
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
mainfile = advfolder+"main.agez" #Initially it is assumed that the agez files are in the script directory (i.e. there is one adventure)
advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
mpc = dot+sep+"mpc-hc.exe"
aplayer = access(mpc, R_OK) #A variable that tests whether Media Player Classic is available
kpic = dot+sep+"kpic.exe"
gviewer = access(kpic, R_OK) #A variable that tests whether KPic is available
if (access(advsfolder, R_OK)) and (str(listdir(advsfolder)) != "[]") : #If there is a non-empty folder called 'Adventures' in the script folder
	if aplayer == True :
		aztheme = dot+sep+"aztheme.aza"
		if access(aztheme, R_OK) :
			playtheme = Popen([mpc, aztheme]) #Will play the theme for Agenzig if MPC is available and theme (aztheme.aza) exists
			sleep(0.5) #Gives time for MPC to launch otherwise it would interupt/minimise the splash screen
	if gviewer == True :
		azsplash = dot+sep+"azsplash.azg"
		if access(azsplash, R_OK) :		
			viewsplash = Popen([kpic, azsplash]) #Will display the splash screen for Agenzig if KPic is available and theme (azsplash.azg) exists
			sleep(3)
			viewsplash.kill()
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
			choice = raw_input("\nPlease type a number corresponding to the adventure you wish to play >" )
		else :
			choice = raw_input(">")
		repeat = 1
		if choice == "" :
			pass #If user inputs nothing then nothing happens
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
	clr()
elif access(mainfile, R_OK) : # If there is only one adventure that is installed in the script directory
	pass #Has no specific code of it's own as mainfile is defined at beginning
else : #Non-valid situations
	if access(advsfolder, R_OK) :
		print "The Adventures folder exists but contains no Adventure folders\n"
	else :
		print "No Adventures folder found in script directory\n"
	print "No main file found in script directory\n\nIf you only have/play one Agenzig adventure then it's files\n(main.agez, attributes.agez etc) should be in the same directory as agenzig.py\n\nIf you have/play multiple adventures then the files for each should be kept\nin a subfolder of 'Adventures' which itself should be\nin the same directory as agenzig.py\n"
	err = raw_input("If you don't know what this means, then you should probably reinstall") #More informative than a crash...
	if err != "Override" :
		exit(0)
#Below code applies to both valid situations (multiple adventures in seperate folders and single adventure in script folder)
main = ConfigObj(mainfile, unrepr=True)
scenefile = advfolder+sep+"scenes.agez"
if access(scenefile, R_OK) : #Main.agez and scenes.agez are bare minimum for an adventure
	scenes = ConfigObj(scenefile, unrepr=True)
	advname = main['Details']['title']
	charfolder = advfolder+"Characters"+sep
	print advname+" succesfully loaded\n"
else :
	err = raw_input("Scenes file missing! This is not a valid adventure")
	if err != "Override" :
		exit(0)
if access(advfolder+"Graphics"+sep, R_OK) :
	graphics = advfolder+"Graphics"+sep
else :
	graphics = 0
if aplayer == True :
	theme = dot+sep+"theme.aza"
	if access(theme, R_OK) :
		playtheme = Popen([mpc, theme]) #Will play the theme for the adventure if MPC is available and theme exists in adventure folder
		sleep(0.5)
if gviewer == True :
	splash = advfolder+"splash.azg"
	if access(splash, R_OK) :		
		viewsplash = Popen([kpic, splash]) #Will display the splash screen for the adventure if KPic is available and theme exists in adventure folder
		sleep(3)
		viewsplash.kill()
charchosen = 0
if not path.exists(charfolder):
    makedirs(charfolder) #Creates a character folder if it does not exist as following code requires it
while charchosen == 0 :
	chars = listdir(charfolder)
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
			if sel < opt :
				chars2 = listdir(charfolder)
				charfile = str(chars2.pop((sel-1)))
				charname = charfile[:-4]
				charfile = charfolder+sep+charfile
				character = ConfigObj(charfile, unrepr=True)
				charchosen = 1
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
equipslots = character['Items']['Equipment'].keys()
equipment = character['Items']['Equipment'].values()
inventory = character['Items']['inventory']
# Loading other files if they exist
choicefile = advfolder+sep+"choices.agez"
if access(choicefile, R_OK) :
	choices = ConfigObj(choicefile, unrepr=True)
else :
	choices = 0
confrontationfile = advfolder+sep+"confrontations.agez"
if access(confrontationfile, R_OK) :
	confrontations = ConfigObj(confrontationfile, unrepr=True)
else :
	confrontations = 0
attributefile = advfolder+sep+"attributes.agez"
if access(attributefile, R_OK) :
	attributes = ConfigObj(attributefile, unrepr=True)
else :
	attributes = 0
vitalfile = advfolder+sep+"vitals.agez"
if access(vitalfile, R_OK) :
	vitals = ConfigObj(vitalfile, unrepr=True)
else :
	vitals = 0
itemfile = advfolder+sep+"items.agez"
if access(vitalfile, R_OK) :
	items = ConfigObj(infile=itemfile, unrepr=True)
else :
	items = 0
equipmentfile = advfolder+sep+"equipment.agez"
if access(equipmentfile, R_OK) :
	equips = ConfigObj(equipmentfile, unrepr=True)
else :
	equips = 0
fight = 0 #Will use to disable combat while is a WIP
vittotal = len(vitals.keys())
if vittotal == 0 : #If Vitals file contains no Vitals
	vitals = 0
attotal = len(attributes.keys())
if attotal == 0 : #If Attributes file contains no Attributes
	attributes = 0
#These are mostly used for while loops and repetition checks
scenechanged = 0
statusgen = 0
sstatusgen = 0
invlistgen = 0
equiplistgen = 0
invchanged = 0
statchanged = 0
equipchanged = 0
#More imports...
from decimal import Decimal
from math import ceil
if sel!= opt : #If user has chosen an existing character rather than creating a new one
	print "Continuing adventure\n"
while True : #Primary game loop - all code above is only for setup and never needs to be reset/run-again
	clr()
	if	scene in (character['Scene States'].keys()) : #If character file has noted that the scenestate of the current scene is different from default
		scenestate = str(character['Scene States'][scene])
	else :
		scenestate = str(1) #Else set scenestate to default (1)
	print scenes[scene][scenestate]['description']
	scenechoicecodes = scenes[scene][scenestate]['choices']
	choicecodes = list(scenes[scene][scenestate]['choices'])
	choicetotal = len(scenechoicecodes)
	choiceno = 0
	while choiceno != choicetotal :
		choiceno += 1
		choicecode = scenechoicecodes[choiceno-1]
		schoicecode = str(choicecode)
		reqtotal = choices[schoicecode]['Requirements']['total']
		reqno = 0
		reqpass = 1
		while reqno != reqtotal :
			reqno += 1
			sreqno = str(reqno)
			if choices[schoicecode]['Requirements'][sreqno]['type'] == 'vital' :
				id = choices[schoicecode]['Requirements'][sreqno]['id']
				evaluator = choices[schoicecode]['Requirements'][sreqno]['evaluator']
				value = choices[schoicecode]['Requirements'][sreqno]['value']
				check = str(character['Vitals'][id])+evaluator+str(value)			
				if eval(check) == False : 
					reqpass = 0
					reqno = reqtotal
			elif choices[schoicecode]['Requirements'][sreqno]['type'] == 'attribute' :
				id = choices[schoicecode]['Requirements'][sreqno]['id']
				evaluator = choices[schoicecode]['Requirements'][sreqno]['evaluator']
				value = choices[schoicecode]['Requirements'][sreqno]['value']
				check = str(character['Attributes'][id])+evaluator+str(value)			
				if eval(check) == False : 
					reqpass = 0
					reqno = reqtotal
			elif choices[schoicecode]['Requirements'][sreqno]['type'] == 'item' :
				evaluator = choices[schoicecode]['Requirements'][sreqno]['evaluator']
				id = int(choices[schoicecode]['Requirements'][sreqno]['id'])
				if (id in inventory) != eval(evaluator) :
					reqpass = 0
					reqno = reqtotal
			elif choices[schoicecode]['Requirements'][sreqno]['type'] == 'equip' :
				evaluator = choices[schoicecode]['Requirements'][sreqno]['evaluator']
				id = int(choices[schoicecode]['Requirements'][sreqno]['id'])
				if (id in equipment) != eval(evaluator) :
					reqpass = 0
					reqno = reqtotal
		if reqpass == 0 :
			choicecodes.remove(choicecode)
	choicesleft = len(choicecodes)
	opt = 0
	scenechoices = ""
	while choicesleft != 0 :
		opt = opt+1
		schoicecode = str(choicecodes.pop())
		choicesleft = len(choicecodes)
		achoicedesc = choices[schoicecode]['description']
		achoice = str(opt)+") "+achoicedesc+"\n"
		scenechoices = scenechoices+achoice
	print "\n"+scenechoices
	sceneb = scene
	scenestateb = scene
	while scenechanged == 0 : #The second stage loop. This is only left, and the code above run when the scene or scene state changes
		prompt = raw_input(">") #The main prompt!
		prompt = prompt.lower() #Make input all lower case
		if prompt == "" :
			pass #If user presses enter without typing anything, do nothing
		elif ((prompt == "choices") or (prompt == "c")) and (choices != 0) :
			print "\n"+scenechoices #Re-print scene choices
		elif ((prompt == 'status') or (prompt == "s")) and (vitals != 0) and (attributes != 0):
			if (statusgen != 1) :
				statuslist = "You are:\n"
				vitno = 0
				while (vitno != vittotal) and (vitals != 0) :
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
				while (attno != attotal) and (attributes != 0) :
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
								descno = '1'
							attlevel = attributes[sattno]['Descriptors']['lessthanbase'][descno]['text']
						elif character['Attributes'][sattno] > basemax :
							highdescsec = Decimal(attributes[sattno]['maxval']-basemax)/attributes[sattno]['Descriptors']['morethanbase']['total']
							descno = str(int(ceil((character['Attributes'][sattno]-basemax)/highdescsec)))
							if int(descno) < 1 :
								descno = '1'
							attlevel = attributes[sattno]['Descriptors']['morethanbase'][descno]['text']
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
				statchanged = 0
			print statuslist
		elif (prompt == 'equipment') or (prompt == "e") :
			if (equiplistgen != 1) : #Checks to see if list of equipment is already generated (i.e. command has been run before) in which case it simply prints it
				tempequipment = []
				for element in equipment :
					if element not in tempequipment : #Removes duplicates as following code assumes no duplicates
						tempequipment.append(element)
				equiptotal = len(tempequipment)
				if equiptotal == 0 :
					equipmentlist = "You have nothing equipped"
				else :
					equiprem = len(tempequipment)
					equipmentlist = "You have equipped:\n"
					tempequipment.reverse()
					while equiprem > 0 :
						aequipno = tempequipment[equiprem-1]
						equiptotal = len(tempequipment)
						equiprem -= 1
						aequipdesc = equips[str(aequipno)]['name']
						equipmentlist = equipmentlist+aequipdesc+"\n"
					equiplistgen = 1
			print equipmentlist
		elif (prompt == "inventory") or (prompt == "i") or (prompt.startswith("use ") and  (len(prompt) > 4)) or (prompt.startswith("equip ") and  (len(prompt) > 6)) : #Inventory list must be generated for items to be used/equipped so commands are combined
			if prompt.startswith("use ") :
				printinv = 0
				comtext = "Use"
				usecode = prompt[4:] #Strips 'use ' to give item code
			elif prompt.startswith("equip ") :
				printinv = 0
				comtext = "Use"
				usecode = prompt[6:] #Strips 'equip ' to give item code
			else :
				printinv = 1
			if invlistgen != 1 :
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
					print "You are not carrying anything of note"
					printinv = 3
				else :
					tempinventory = []
					for element in inventory :
						if element not in tempinventory : #Removes duplicates as following code assumes no duplicates
							tempinventory.append(element)
				invlistgen = 1
			elif opt == 0 :
				print "You are not carrying anything of note"
				printinv = 3
			if printinv == 1:
				print "\n"+inventorylist
			elif printinv == 0 :
				if usecode.isdigit() == 1 :
					usecode = int(usecode)
					if usecode <= opt :
						useditem = str(tempinventory[usecode-1])
						reqtotal = items[useditem]['Requirements']['total']
						reqno = 0
						reqpass = 1
						while reqno != reqtotal : #Checking requirements of the used item
							reqno += 1
							sreqno = str(reqno)
							if items[useditem]['Requirements'][sreqno]['type'] == 'vital' :
								id = items[useditem]['Requirements'][sreqno]['id']
								evaluator = items[useditem]['Requirements'][sreqno]['evaluator']
								value = items[useditem]['Requirements'][sreqno]['value']
								check = str(character['Vitals'][id])+evaluator+str(value)			
								if eval(check) == False : 
									reqpass = 0
									reqno = reqtotal
							elif items[useditem]['Requirements'][sreqno]['type'] == 'attribute' :
								id = items[useditem]['Requirements'][sreqno]['id']
								evaluator = items[useditem]['Requirements'][sreqno]['evaluator']
								value = items[useditem]['Requirements'][sreqno]['value']
								check = str(character['Attributes'][id])+evaluator+str(value)			
								if eval(check) == False : 
									reqpass = 0
									reqno = reqtotal
							elif items[useditem]['Requirements'][sreqno]['type'] == 'item' :
								evaluator = items[useditem]['Requirements'][sreqno]['evaluator']
								id = int(items[useditem]['Requirements'][sreqno]['id'])
								if (id in inventory) != eval(evaluator) :
									reqpass = 0
									reqno = reqtotal
							elif items[useditem]['Requirements'][sreqno]['type'] == 'equip' :
								evaluator = items[useditem]['Requirements'][sreqno]['evaluator']
								id = int(items[useditem]['Requirements'][sreqno]['id'])
								if (id in equipment) != eval(evaluator) :
									reqpass = 0
									reqno = reqtotal
						if reqpass == 1 :
							print items[useditem]['usetext']
							if items[useditem]['singleuse'] == 1 :
								inventory.remove(int(useditem))
								invchanged = 1
							effecttotal = items[useditem]['Effects']['total']
							effectno = 0
							while effectno != effecttotal :
								effectno += 1
								seffectno = str(effectno)
								if (items[useditem]['Effects'][seffectno]['type'] == 'vital') or (items[useditem]['Effects'][seffectno]['type'] == 'vitalrestore'):
									id = items[useditem]['Effects'][seffectno]['id']
									operator = items[useditem]['Effects'][seffectno]['operator']
									value = items[useditem]['Effects'][seffectno]['value']
									exec("character['Vitals'][id]"+operator+str(value))					
									statchanged = 1
									if (items[useditem]['Effects'][seffectno]['type'] == 'vitalrestore') and (character['Vitals'][id] > character['Vitals']['Initial Values'][id]) :
										character['Vitals'][id] = character['Vitals']['Initial Values'][id]
								elif (items[useditem]['Effects'][seffectno]['type'] == 'attribute') or (items[useditem]['Effects'][seffectno]['type'] == 'attributerestore'):
									id = items[useditem]['Effects'][seffectno]['id']
									operator = items[useditem]['Effects'][seffectno]['operator']
									value = items[useditem]['Effects'][seffectno]['value']
									exec("character['Attributes'][id]"+operator+str(value))
									statchanged = 1
									if (items[useditem]['Effects'][seffectno]['type'] == 'attributerestore') and (character['Attributes'][id] > character['Attributes']['Initial Values'][id]) :
										character['Attributes'][id] = character['Attributes']['Initial Values'][id]
								elif items[useditem]['Effects'][seffectno]['type'] == 'additem' :
									id = items[useditem]['Effects'][seffectno]['id']
									value = items[useditem]['Effects'][seffectno]['value']
									for _ in repeat(None, value) :
										inventory.append(int(id))
									invchanged = 1
								elif items[useditem]['Effects'][seffectno]['type'] == 'equip' :
									id = items[useditem]['Effects'][seffectno]['id']
									slotsused = equips[id]['equipslots']
									charequips = character['Items']['Equipment']
									replaceditems = []
									for slotx in slotsused :
										if str(slotx) in equipslots : #If there is already a piece of equipment occupying the slot
											replacedequip = charequips[str(slotx)]
											if (equips[replacedequip]['equipslots'] != equips[id]['equipslots']) and (equips[replacedequip]['equipslots'] != [slotx]) :
												for clearslot in equips[replacedequip]['equipslots'] :
													clearslot = str(clearslot)
													if clearslot != slotx :
														del character['Items']['Equipment'][clearslot]
														equipslots = character['Items']['Equipment'].keys()
											replaceditem = str(equips[replacedequip]['item'])
											if replaceditem not in replaceditems :
												inventory.append(int(replaceditem))
												replaceditems.append(replaceditem)
										charequips[str(slotx)] = id
									invchanged = 1
									equipchanged = 1
						elif reqpass == 0 :
							print items[useditem]['Requirements'][sreqno]['failtext']
					else :
						print "You are only carrying "+str(len(inventory))+" types of item"
				else :
					print comtext+" command must be followed by a number"
		elif (prompt == "help") or (prompt == "h") or (prompt == "man") :
			print "\nCommand List"
			print "'choices': review availible options"
			print "'inventory': view your inventory"
			print "'equipment': view what items you have equipped"
			print "'use #': Use or equip item with the number #"
			print "'status': view the statuses of your vitals and attributes"
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
		if (scene != sceneb) or (scenestate != scenestateb) or (invchanged == 1) or (statchanged == 1) or (equipchanged == 1):
			character.write()
			if (scene != sceneb) or (scenestate != scenestateb) :
				scenechanged = 1
			if invchanged == 1 :
				invlistgen = 0
				invchanged = 0
			if statchanged == 1 :
				statusgen = 0
			if equipchanged == 1 :
				equiplistgen = 0
				equipslots = character['Items']['Equipment'].keys()
				equipment = character['Items']['Equipment'].values()