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
	from configobj import * #I'm using configobj instead of the built-in Configeditor as it allows for nested sections and list values
except ImportError, e:
	err = raw_input("ConfigObj module is required. Please install and try again")
	if err != "Override" :
		exit(0)
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
		clr()
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
		print "Input must be a number\n"
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
	scenechoices = []
	while choicesleft != 0 :
		opt = opt+1
		schoicecode = str(choicecodes.pop())
		choicesleft = len(choicecodes)
		achoicedesc = choices[schoicecode]['description']
		achoice = str(opt)+") "+achoicedesc
		scenechoices.append(achoice)
	print '\n'.join(scenechoices)
	sceneb = scene
	scenestateb = scene
	while scenechanged == 0 : #The second stage loop. This is only left, and the code above run when the scene or scene state changes
		prompt = raw_input(">").lower() #The main prompt!
		#clr()
		splitprompt = prompt.split(' ',1)
		promptcomm = splitprompt[0]
		if len(splitprompt) > 1 :
			promptval = splitprompt[1]
		else :
			promptval = '-'
		if prompt == "" :
			pass #If user presses enter without typing anything, do nothing
		elif ((prompt == "choices") or (prompt == "c")) and (choices != 0) :
			print '\n'.join(scenechoices) #Re-print scene choices
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
				for aequip in equipment :
					if aequip not in tempequipment : #Removes duplicates as following code assumes no duplicates
						tempequipment.append(aequip)
				equiptotal = len(tempequipment)
				if equiptotal == 0 :
					equipmentlist = ["You have nothing equipped"]
				else :
					equipmentlist = ["You have equipped:"]
					for aequipno in tempequipment :
						aequipdesc = equips[str(aequipno)]['description']
						equipmentlist.append(aequipdesc)
					equiplistgen = 1
			print '\n'.join(equipmentlist)
		elif  promptcomm in main['Commands']['Items']['removing'].keys() and promptval.replace(' ', '').isalpha() :
			if len(equipment) > 0 :
				tempequipment = list(set(equipment))
				temp2equipment = []
				for aequip in tempequipment :
					if promptcomm in equips[aequip]['removewords'] :
						temp2equipment.append(aequip)
				if len(temp2equipment) > 0 :
					potentialequips = []
					for aequip in temp2equipment :
						if (promptval == equips[aequip]['description'].lower()) or (promptval in equips[aequip]['altdescs']) :
							potentialequips.append(aequip)
					if len(potentialequips) > 0 :
						if len(potentialequips) == 1 :						
							equiptoremove = potentialequips[0]
						else :
							print "Which %s do you want to %s?" %(promptval, promptcomm)
							potentialequipdescs = []
							for aequip in potentialequips :
								potentialequipdescs.append(equips[aequip]['description'])
							print '\n'.join(potentialequipdescs)
							prompt = raw_input(">")
							if prompt.isdigit() :
								if int(prompt) <= len(potentialequips) :
									equiptoremove = potentialequips[int(prompt)-1]
								else :
									equiptoremove = 0
							elif prompt.isalpha and prompt != 'help':
								equiptoremove = 0
								for aequip in potentialequips :
									if (prompt.lower() == items[str(aequip)]['description'].lower()) :
										equiptoremove = aequip
							else :
								equiptoremove = 0
						if equiptoremove > 0 :
							itemtoadd = equips[equiptoremove]['item']								
							clearslots = equips[equiptoremove]['equipslots']
							for clearslot in clearslots :
								del character['Items']['Equipment'][str(clearslot)]
							inventory.append(itemtoadd)
							print equips[equiptoremove]['removetext']
							invchanged = 1
							equipchanged = 1
						else :
							#clr()
							print "Enter either a number coresponding to the position of a item on the list or the complete description of a listed item"
					else :
						print main['Commands']['Items']['removing'][promptcomm]['fail_b']
				else :
					print main['Commands']['Items']['removing'][promptcomm]['fail_a']
			else :
				print main['Commands']['Items']['removing'][promptcomm]['fail_a']
		elif (prompt == "inventory") or (prompt == "i") : #This command simply prints the character's inventory in lsit form
			if invlistgen != 1 :
				printeditems = []
				if len(inventory) == 0 :
					inventorylist = ['You are not carrying anything of note']
				else :
					inventorylist = ['You are carrying:']
					for aitem in inventory :
						if printeditems.count(aitem) == 0 : #Ignores items that have already been processed
							aitemocc = inventory.count(aitem)
							aitemdesc = items[str(aitem)]['description']
							if aitemocc > 1 : #If there are multiple copies of the same item
								inventorylist.append(aitemdesc+" x "+str(aitemocc)) #Puts 'x #' next to the item where '#' is the number of copies
							else :
								inventorylist.append(aitemdesc)
							printeditems.append(aitem)
				invlistgen = 1
				print '\n'.join(inventorylist)
		elif (promptcomm in main['Commands']['Items']['using'].keys() or promptcomm in main['Commands']['Items']['equipping'].keys()) and promptval.replace(' ', '').isalpha() :
			tempinventory = list(inventory)
			if promptcomm not in promptcomm in main['Commands']['Items']['equipping'].keys() :
				for aequip in equipment :
					tempinventory.append(equips[aequip]['item'])
			temp2inventory = []
			for element in tempinventory :
				if element not in temp2inventory :
					temp2inventory.append(element)
			tempinventory = []
			for element in temp2inventory :
				if promptcomm in items[str(element)]['Actions'].keys() :
					tempinventory.append(element)
			if len(tempinventory) == 0 :
				#clr()
				print "No items you possess can be used in that way\n" #Will soft-code
				useditem = 0
			else :
				potentialitems = []
				for element in tempinventory :
					if (promptval == items[str(element)]['description'].lower()) or (promptval in items[str(element)]['altdescs']) :
						potentialitems.append(element)
				if len(potentialitems) == 0 :
					#clr()
					print "No items you possess that match that description can be used in that way\n" #Will soft-code
					useditem = 0
				elif len(potentialitems) == 1 :
					useditem = potentialitems[0]
				else :
					print "Which %s do you want to %s?" %(promptval, promptcomm)
					potentialitemdescs = []
					for element in potentialitems :
						potentialitemdescs.append(items[str(element)]['description'])
					print '\n'.join(potentialitemdescs)
					prompt = raw_input(">").lower()
					if prompt.isdigit() :
						if int(prompt) <= len(potentialitems) :
							useditem = potentialitems[int(prompt)-1]
						else :
							#clr()
							print "You only possess %s %s that can be %s\n" %(len(potentialitems), promptval, promptcomm)
							useditem = 0
					else :
						useditem = -1
						for element in potentialitems :
							if prompt == items[str(element)]['description'].lower() :
								useditem = element
			reqpass = -1
			if useditem > 0 :
				useditem = str(useditem)
				itemreqs = items[useditem]['Actions'][promptcomm]['Requirements'].keys()
				reqpass = 1
				for reqno in itemreqs :
					sreqno = str(reqno)
					id = items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['id']
					evaluator = items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['evaluator']
					if items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['type'] == 'vital' :
						value = items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['value']
						check = str(character['Vitals'][id])+evaluator+str(value)			
						if eval(check) == False : 
							reqpass = 0
							break
					elif items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['type'] == 'attribute' :
						value = items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['value']
						check = str(character['Attributes'][id])+evaluator+str(value)			
						if eval(check) == False : 
							reqpass = 0
							break
					elif items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['type'] == 'item' :
						if (int(id) in inventory) != eval(evaluator) :
							reqpass = 0
							break
					elif items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['type'] == 'equip' :
						if (int(id) in equipment) != eval(evaluator) :
							reqpass = 0
							break
			elif useditem < 0 :
				#clr()
				print "None of the listed items match that exact description"
			if reqpass == 1 :
				print items[useditem]['Actions'][promptcomm]['Details']['text']
				if items[useditem]['Actions'][promptcomm]['Details']['singleuse'] == 1 :
					inventory.remove(int(useditem))
					invchanged = 1
				itemeffects = items[useditem]['Actions'][promptcomm]['Effects'].keys()
				for effectno in itemeffects :
					seffectno = str(effectno)
					id = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['id']
					if items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] != 'equip' : value = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['value']
					if items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] == 'vital' :
						operator = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['operator']
						exec("character['Vitals'][id]"+operator+str(value))					
						statchanged = 1
					elif (items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] == 'vitalrestore') and (character['Vitals'][id] < character['Vitals']['Initial Values'][id]):
						exec("character['Vitals'][id]+="+str(value))
						if character['Vitals'][id] > character['Vitals']['Initial Values'][id] : character['Vitals'][id] = character['Vitals']['Initial Values'][id] 
						statchanged = 1
					elif items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] == 'attribute' :
						operator = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['operator']
						exec("character['Attributes'][id]"+operator+str(value))
						statchanged = 1
					elif (items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] == 'attributerestore') and (character['Attributes'][id] < character['Attributes']['Initial Values'][id]) :
						exec("character['Attributes'][id]+="+str(value))
						if character['Attributes'][id] > character['Attributes']['Initial Values'][id] : character['Attributes'][id] = character['Attributes']['Initial Values'][id] 
						statchanged = 1
					elif items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] == 'additem' :
						for _ in repeat(None, value) :
							inventory.append(int(id))
						invchanged = 1
					elif items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type'] == 'equip' :
						id = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['id']
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
				print items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['failtext']
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
		elif promptcomm in main['Commands']['Items']['using'].keys() or promptcomm in promptcomm in main['Commands']['Items']['equipping'].keys():
			if promptval.isdigit() :
				print "'%s' should be followed by all or part of the description of an item - not a number" %(promptcomm)
			else :
				print "'%s' should be followed by all or part of the description of an item" %(promptcomm)
		else :
			print main['Messages']['unknowncommand']
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