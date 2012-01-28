#-------------------------------------------------------------------------------
# Name:        Agenzig Main Script
# Purpose:     Text-based adventure game engine
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
	import configobj
except ImportError, e:
	raw_input("ConfigObj module is required. Please install and try again")
	exit(0)
from configobj import *
dot = str(os.curdir) #The character used by the current os to denote the current folder. Is '.' in Windows
sep = str(os.sep) #The character used by the current os to denote the demotion to another folder level. Is '/' in Windows
mainfile = dot+sep+"main.agez"
advsfolder = "%s%sAdventures%s" %(dot,sep,sep)
if os.access(mainfile, os.R_OK) :
	main = ConfigObj(mainfile, unrepr=True)
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
	main = ConfigObj(mainfile, unrepr=True)
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
	opt = 1
	if charsno != 0 :
		print "Listing characters"
		while charsno != 0 :
			print "%s) %s" %(opt,chars.pop())
			charsno = charsno-1
			opt = opt+1
		print ""
		print "%s) New Character" %(opt)
		print ""
		choice = raw_input("Please type a number corresponding to the above option you require" )
	else :
		print "No characters found"
		print "Initiating character creation"
		choice = str(1)
	if choice.isdigit() == 1 :
		sel = int(choice)
		if sel == opt :
			charname = raw_input("Please enter a name for your character: " )
			genderin = raw_input("Is your character Male of Female? " )
			genderin = genderin.lower()
			if (genderin == "male") or (genderin == "m") or (genderin == "ma") or (genderin == "mas") :
				chargender = "male"
			elif (genderin == "female") or (genderin == "f") or (genderin == "fe") or (genderin == "fem") :
				chargender = "female"
			else :
				print "I'll take that to mean your character is gender neutral"
				chargender = "neutral"
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
character = ConfigObj(charfile, unrepr=True)
if sel == opt : #Making a new character
	csetup = main['Character Setup']
	character['Basics'] = {}
	character['Basics']['charname'] = charname
	character['Basics']['gender'] = chargender
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
inventory = character['Items']['inventory']
# Loading other files
scenefile = advfolder+sep+"scenes.agez"
scenes = ConfigObj(scenefile, unrepr=True)
choicefile = advfolder+sep+"choices.agez"
choices = ConfigObj(choicefile, unrepr=True)
confrontationfile = advfolder+sep+"confrontations.agez"
confrontations = ConfigObj(confrontationfile, unrepr=True)
itemfile = advfolder+sep+"items.agez"
items = ConfigObj(infile=itemfile, unrepr=True)
armourfile = advfolder+sep+"armour.agez"
armours = ConfigObj(armourfile, unrepr=True)
mweaponfile = advfolder+sep+"mweapons.agez"
mweapons = ConfigObj(mweaponfile, unrepr=True)
rweaponfile = advfolder+sep+"rweapons.agez"
rweapons = ConfigObj(rweaponfile, unrepr=True)
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
	print ""
	print scenechoices
	sceneb = scene
	scenestateb = scene
	scenechanged = 0
	statusgen = 0
	invlistgen = 0
	itemused = 0
	from decimal import *
	while scenechanged == 0 :
		prompt = raw_input("") #The main prompt!
		prompt = prompt.lower()
		if prompt == "" :
			pass
		elif (prompt == "choices") or (prompt == "c") :
			print ""
			print scenechoices
		elif  (prompt == "status") or (prompt == "s") :
			if statusgen != 1 :
				if health > ((int(main['Attribute Categories']['healthy'])/10)*12) :
					stathealth = "You are EXTREMELY Healthy\n"
				elif (health > int(main['Attribute Categories']['healthy'])) and (health <=  ((int(main['Attribute Categories']['healthy']))/10)*12) :
					stathealth = "You are Unnaturally Healthy\n"
				elif (health <= int(main['Attribute Categories']['healthy'])) and (health >= ((int(main['Attribute Categories']['healthy']))/10)*8) :
					stathealth = "You are Healthy\n"
				elif health >= ((int(main['Attribute Categories']['healthy']))/10)*6 :
					stathealth = "You are Hurt\n"
				elif health >= ((int(main['Attribute Categories']['healthy']))/10)*4 :
					stathealth = "You are Injured\n"
				elif health >= ((int(main['Attribute Categories']['healthy']))/10)*2 :
					stathealth = "You are Severely Injured\n"
				elif health > 0 :
					stathealth = "You are Near Death\n"
				else :
					stathealth = "How are you alive?\n"
				if fatigue < 0 :
					statfatigue = "You are Extraordinarily Energetic\n"
				elif fatigue == 0 :
					statfatigue = "You are Full of Energy\n"
				elif fatigue <= ((int(main['Attribute Categories']['debilitatingfatigue']))/10)*1 :
					statfatigue = "You are Mildly Fatigued\n"
				elif fatigue <= ((int(main['Attribute Categories']['debilitatingfatigue']))/10)*2 :
					statfatigue = "You are Weary\n"
				elif fatigue <= ((int(main['Attribute Categories']['debilitatingfatigue']))/10)*4 :
					statfatigue = "You are Tired\n"
				elif fatigue <= ((int(main['Attribute Categories']['debilitatingfatigue']))/10)*6 :
					statfatigue = "You are Worn Out\n"
				elif fatigue <= ((int(main['Attribute Categories']['debilitatingfatigue']))/10)*8 :
					statfatigue = "You are Exhausted\n"
				elif fatigue > int(main['Attribute Categories']['debilitatingfatigue']) :
					statfatigue = "You are Totally Cream Crackered\n"
				else :
					statfatigue = "You are beyond exhausation\n"
				if (strength >= int(main['Attribute Categories']['strong'])/10*9) and (strength <= int(main['Attribute Categories']['strong'])/10*11) :
					statstrength = "You are Strong\n"
				elif strength > int(main['Attribute Categories']['strong'])/10*11 :
					if strength < int(main['Attribute Categories']['strong'])/10*13.3 :
						statstrength = "You are Very Strong\n"
					elif strength < int(main['Attribute Categories']['strong'])/10*15.6 :
						statstrength = "You are Mighty\n"
					elif strength < int(main['Attribute Categories']['strong'])/10*17.9 :
						statstrength = "You are Immensely Strong\n"
					elif strength < int(main['Attribute Categories']['strong'])/10*20 :
						statstrength = "You are Incredibly Strong\n"
					else :
						statstrength = "You are Herculean\n"
				else :
					if strength > int(main['Attribute Categories']['strong'])/10*6.7 :
						statstrength = "You are Diminished\n"
					elif strength > int(main['Attribute Categories']['strong'])/10*4.4 :
						statstrength = "You are Weak\n"
					elif strength > int(main['Attribute Categories']['strong'])/10*2.1 :
						statstrength = "You are Feeble\n"
					elif strength > 0 :
						statstrength = "You are Frail\n"
					else :
						statstrength = "You are Incapacitated\n"		
				if (knowledge >= int(main['Attribute Categories']['knowlegable'])/10*9) and (knowledge <= int(main['Attribute Categories']['knowlegable'])/10*11) :
					statknowledge = "You are Knowledgable\n"
				elif knowledge > int(main['Attribute Categories']['knowlegable'])/10*11 :
					if knowledge < int(main['Attribute Categories']['knowlegable'])/10*13.3 :
						statknowledge = "You are Very knowledgable\n"
					elif knowledge < int(main['Attribute Categories']['knowlegable'])/10*15.6 :
						statknowledge = "You are Highly Educated\n"
					elif knowledge < int(main['Attribute Categories']['knowlegable'])/10*17.9 :
						statknowledge = "You are Learned\n"
					elif knowledge < int(main['Attribute Categories']['knowlegable'])/10*20 :
						statknowledge = "You are Enlightened\n"
					else :
						statknowledge = "You are Omniscient\n"
				else :
					if knowledge > int(main['Attribute Categories']['knowlegable'])/10*6.7 :
						statknowledge = "You are Poorly Educated\n"
					elif knowledge > int(main['Attribute Categories']['knowlegable'])/10*4.4 :
						statknowledge = "You are Dumb\n"
					elif knowledge > int(main['Attribute Categories']['knowlegable'])/10*2.1 :
						statknowledge = "You are Ignorant\n"
					elif knowledge > 0 :
						statknowledge = "You are Naive\n"
					else :
						statknowledge = "You are Vegetative\n"
				if (dexterity >= int(main['Attribute Categories']['knowlegable'])/10*9) and (dexterity <= int(main['Attribute Categories']['knowlegable'])/10*11) :
					statdexterity = "You are Dexterous\n"
				elif dexterity > int(main['Attribute Categories']['knowlegable'])/10*11 :
					if dexterity < int(main['Attribute Categories']['knowlegable'])/10*13.3 :
						statdexterity = "You are Deft\n"
					elif dexterity < int(main['Attribute Categories']['knowlegable'])/10*15.6 :
						statdexterity = "You are Precise\n"
					elif dexterity < int(main['Attribute Categories']['knowlegable'])/10*17.9 :
						statdexterity = "You are Highly Dexterous\n"
					elif dexterity < int(main['Attribute Categories']['knowlegable'])/10*20 :
						statdexterity = "You are Extremely Deft\n"
					else :
						statdexterity = "You Move Faster Than The Eye Can See\n"
				else :
					if dexterity > int(main['Attribute Categories']['knowlegable'])/10*6.7 :
						statdexterity = "You are Gawky\n"
					elif dexterity > int(main['Attribute Categories']['knowlegable'])/10*4.4 :
						statdexterity = "You are Ungainly\n"
					elif dexterity > int(main['Attribute Categories']['knowlegable'])/10*2.1 :
						statdexterity = "You are Clumsy\n"
					elif dexterity > 0 :
						statdexterity = "You are Highly Cumbersome\n"
					else :
						statdexterity = "You are Completely Uncoordinated\n"
				if (willpower >= int(main['Attribute Categories']['determined'])/10*9) and (willpower <= int(main['Attribute Categories']['determined'])/10*11) :
					statwillpower = "You are Determined\n"
				elif willpower > int(main['Attribute Categories']['determined'])/10*11 :
					if willpower < int(main['Attribute Categories']['determined'])/10*13.3 :
						statwillpower = "You are Steadfast\n"
					elif willpower < int(main['Attribute Categories']['determined'])/10*15.6 :
						statwillpower = "You are Unshakable\n"
					elif willpower < int(main['Attribute Categories']['determined'])/10*17.9 :
						statwillpower = "You are Highly Dexterous\n"
					elif willpower < int(main['Attribute Categories']['determined'])/10*20 :
						statwillpower = "You are Extremely Deft\n"
					else :
						statwillpower = "You Move Faster Than The Eye Can See\n"
				else :
					if willpower > int(main['Attribute Categories']['determined'])/10*6.7 :
						statwillpower = "You are Suggestable\n"
					elif willpower > int(main['Attribute Categories']['determined'])/10*4.4 :
						statwillpower = "You are Weak-willed\n"
					elif willpower > int(main['Attribute Categories']['determined'])/10*2.1 :
						statwillpower = "You are Obedient\n"
					elif willpower > 0 :
						statwillpower = "You are Robotic\n"
					else :
						statwillpower = "You are Completely Uncoordinated\n"	
				if (constitution >= int(main['Attribute Categories']['built'])/10*9) and (constitution <= int(main['Attribute Categories']['built'])/10*11) :
					statconstitution = "You are Built\n"
				elif constitution > int(main['Attribute Categories']['built'])/10*11 :
					if constitution < int(main['Attribute Categories']['built'])/10*13.3 :
						statconstitution = "You are Fortified\n"
					elif constitution < int(main['Attribute Categories']['built'])/10*15.6 :
						statconstitution = "You are Highly Resilient\n"
					elif constitution < int(main['Attribute Categories']['built'])/10*17.9 :
						statconstitution = "You are Unassailable\n"
					elif constitution < int(main['Attribute Categories']['built'])/10*20 :
						statconstitution = "You are Impenetrable\n"
					else :
						statconstitution = "You are WICKED SICK\n"
				else :
					if constitution > int(main['Attribute Categories']['built'])/10*6.7 :
						statconstitution = "You are Underweight\n"
					elif constitution > int(main['Attribute Categories']['built'])/10*4.4 :
						statconstitution = "You are Stunted\n"
					elif constitution > int(main['Attribute Categories']['built'])/10*2.1 :
						statconstitution = "You are Scrawny\n"
					elif constitution > 0 :
						statconstitution = "You are Falling Apart\n"
					else :
						statconstitution = "You are Incorporeal\n"
				if (charisma >= int(main['Attribute Categories']['charismatic'])/10*9) and (charisma <= int(main['Attribute Categories']['charismatic'])/10*11) :
					statcharisma = "You are Charismatic\n"
				elif charisma > int(main['Attribute Categories']['charismatic'])/10*11 :
					if charisma < int(main['Attribute Categories']['charismatic'])/10*13.3 :
						statcharisma = "You are Persuasive\n"
					elif charisma < int(main['Attribute Categories']['charismatic'])/10*15.6 :
						statcharisma = "You are Imposing\n"
					elif charisma < int(main['Attribute Categories']['charismatic'])/10*17.9 :
						statcharisma = "You are Distinguished\n"
					elif charisma < int(main['Attribute Categories']['charismatic'])/10*20 :
						statcharisma = "You are Eminent\n"
					else :
						statcharisma = "You are Awe-inspiring\n"
				else :
					if charisma > int(main['Attribute Categories']['charismatic'])/10*6.7 :
						statcharisma = "You are Unheeded\n"
					elif charisma > int(main['Attribute Categories']['charismatic'])/10*4.4 :
						statcharisma = "You are Unlikeable\n"
					elif charisma > int(main['Attribute Categories']['charismatic'])/10*2.1 :
						statcharisma = "You are Irritating\n"
					elif charisma > 0 :
						statcharisma = "You are Galling\n"
					else :
						statcharisma = "You are Widely Hated\n"
				if (perception >= int(main['Attribute Categories']['perceptive'])/10*9) and (perception <= int(main['Attribute Categories']['perceptive'])/10*11) :
					statperception = "You are Perceptive\n"
				elif perception > int(main['Attribute Categories']['perceptive'])/10*11 :
					if perception < int(main['Attribute Categories']['perceptive'])/10*13.3 :
						statperception = "You are Keen-eyed\n"
					elif perception < int(main['Attribute Categories']['perceptive'])/10*15.6 :
						statperception = "You are Scanning\n"
					elif perception < int(main['Attribute Categories']['perceptive'])/10*17.9 :
						statperception = "You are Distinguished\n"
					elif perception < int(main['Attribute Categories']['perceptive'])/10*20 :
						statperception = "You are Eminent\n"
					else :
						statperception = "You are Omnipercipient\n"
				else :
					if perception > int(main['Attribute Categories']['perceptive'])/10*6.7 :
						statperception = "You are Unheeded\n"
					elif perception > int(main['Attribute Categories']['perceptive'])/10*4.4 :
						statperception = "You are Illusioned\n"
					elif perception > int(main['Attribute Categories']['perceptive'])/10*2.1 :
						statperception = "You are Irritating\n"
					elif perception > 0 :
						statperception = "You are Galling\n"
					else :
						statperception = "You are Blind\n"							
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
				status = "Current Status:\n"+stathealth+statfatigue+"\n"+statstrength+statknowledge+statdexterity+statwillpower+statconstitution+"\n"+statarmour+statweapons
				statusgen = 1
			print ""
			print status
		elif (prompt == "inventory") or (prompt == "i") or (prompt.startswith("use ") and  (len(prompt) > 4)) :
			if prompt.startswith("use ") :
				printinv = 0
			else :
				printinv = 1
			if (invlistgen != 1)  or (itemused == 1) :
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
				print ""
				print inventorylist
			elif printinv == 0 :
				usecode = prompt.lstrip('u')
				usecode = usecode.lstrip('s')
				usecode = usecode.lstrip('e')
				usecode = usecode.lstrip(' ')
				if choice.isdigit() == 1 :
					usecode = int(usecode)
					if usecode <= opt :
						useditem = str(tempinventory.pop((usecode-1)))
						print useditem
						itemused = 1
					else :
						print "You are only carrying "+str(len(inventory))+" types of item"
				else :
					print "USE command must be followed by a number"
		elif (prompt == "help") or (prompt == "h") or (prompt == "man") :
			print ""
			print "Command List"
			print "'choices': review availible options"
			print "'inventory': view your inventory"
			print "'status': view your health, attributes and equipment"
			print "'help': view these commands again"
		else :
			print "Try using an ACTUAL command moron"  #Might change this before release...
		if (scene != sceneb) or (scenestate != scenestateb) :
			scenechanged = 1