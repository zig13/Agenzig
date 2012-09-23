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
				charfile = str(chars2.pop((sel-1)))
				charname = charfile[:-4]
				charfile = charfolder+sep+charfile
				character = ConfigObj(charfile, unrepr=True)
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
while True : #Basically, you're not getting out of this loop...
	if	scene in character['Scene States'] :
		scenestate = str(character['Scene States'][scene])
	else :
		scenestate = str(1)
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
			elif choices[schoicecode]['Requirements'][sreqno]['type'] == 'equipment' :
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
	scenechanged = 0
	statusgen = 0
	sstatusgen = 0
	invlistgen = 0
	equiplistgen = 0
	itemused = 0
	statchanged = 0
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
				statchanged = 0
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
				comtext = "Use"
				usecode = prompt[4:]
			elif prompt.startswith("equip ") :
				printinv = 0
				comtext = "Use"
				usecode = prompt[6:]
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
					tempinventory = list(inventory)
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
						useditem = str(tempinventory.pop((usecode-1)))
						if items[useditem]['singleuse'] == 1 :
							inventory.remove(int(useditem))
							itemused = 1
						print items[useditem]['usetext']
					else :
						print "You are only carrying "+str(len(inventory))+" types of item"
				else :
					print comtext+" command must be followed by a number"
		elif (prompt == "help") or (prompt == "h") or (prompt == "man") :
			print "\nCommand List"
			print "'choices': review availible options"
			print "'inventory': view your inventory"
			print "'equipment': view what items you have equipped"
			print "'status': view your vitals and attributes"
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
		if (scene != sceneb) or (scenestate != scenestateb) or (itemused == 1) or (statchanged == 1) :
			character.write()
			if (scene != sceneb) or (scenestate != scenestateb) :
				scenechanged = 1
			if itemused == 1 :
				invlistgen = 0
				itemused = 0
			if statchanged == 1 :
				statusgen = 0