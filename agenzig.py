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
from classes.classPath import Path
path = Path()

if path.validate() == False :
	raw_input("No adventures are installed.\nAdventures should be in individual folders inside a directory named 'Adventures' within this one.")
	exit(0)

from functions import Clr, yesno, choicelist
if path.advstotal == 1 :
	from classes.classAdventure import Adventure, validation_fail
	adventure = Adventure(path.adventures[0])
	try :
		adventure.validate()
	except validation_fail as e:
		print e.reason, "from adventure folder.\n"
		raw_input("Please reinstall the adventure")
		exit(0)
else :
	from classes.classAdventure import Adventure, validation_fail
	print "Listing Adventures:"
	while True :
		print "Which adventure would you like to play?"
		choice = list(choicelist(path.adventures))
		try :		
			adventure = Adventure(choice[1])
			adventure.validate()
			break
		except validation_fail as e:
			print e.reason, "\nPlease choose a different adventure\n"

adventure.details()
print "%s successfully loaded" %(adventure.title)

charname = None
while charname == None :
	if adventure.path.chartotal > 0 :
		charopts = list(adventure.path.characters)
		charopts.append("New Character")
		print "What character would you like to load?"
		choice = list(choicelist(charopts))
	else :
		print "No characters exist for this adventure.\nStarting character creation.\n"

	if (adventure.path.chartotal == 0) or (choice[0] == adventure.path.chartotal+1) :
		exec "from charcreators."+adventure.charcreator+" import createchar" #Runs the apropriate character creator for the adventure
		newchar = createchar(adventure.path)
		if bool(newchar[0]) == True :
			print "Character created successfully\nWould you like to load this character now?"
			answer = bool(yesno())
			if answer == True :
				charname = str(newchar[1])+".azc"
		else :
			print "Character creation failed\n"
	else :
		charname = choice[1]
		
from classes.classCharacter import Character
character = Character(adventure.path, charname)

#Setting main and character varibles for easy access
from classes.classScene import Scene
scene = Scene(adventure.path, character.getscene)
scene.setstate(character.checkstate(scene.id))

fight = 0 #Will use to disable combat while is a WIP

#These are mostly used for while loops and repetition checks
statusgen = 0
invlistgen = 0
equiplistgen = 0
invchanged = 0
statchanged = 0
equipchanged = 0

#More imports...
from decimal import Decimal
from math import ceil

while True : #Primary game loop - all code above is only for setup and never needs to be reset/run-again
	print scene.description()
	if choices != 0 :
		choicecodelist = list(scene.choices())
		for choicecode in choicecodelist :
			choicereqs = choices[choicecode]['Requirements'].keys()
			reqpass = 1
			for choicereq in choicereqs :
				if choices[choicecode]['Requirements'][choicereq]['type'] == 'vital' :
					id = choices[choicecode]['Requirements'][choicereq]['id']
					evaluator = choices[choicecode]['Requirements'][choicereq]['evaluator']
					value = choices[choicecode]['Requirements'][choicereq]['value']
					check = str(character['Vitals'][id])+evaluator+str(value)			
					if eval(check) == False : 
						reqpass = 0
				elif choices[choicecode]['Requirements'][choicereq]['type'] == 'attribute' :
					id = choices[choicecode]['Requirements'][choicereq]['id']
					evaluator = choices[choicecode]['Requirements'][choicereq]['evaluator']
					value = choices[choicecode]['Requirements'][choicereq]['value']
					check = str(character['Attributes'][id])+evaluator+str(value)			
					if eval(check) == False : 
						reqpass = 0
				elif choices[choicecode]['Requirements'][choicereq]['type'] == 'item' :
					evaluator = choices[choicecode]['Requirements'][choicereq]['evaluator']
					id = int(choices[choicecode]['Requirements'][choicereq]['id'])
					if (id in inventory) != eval(evaluator) :
						reqpass = 0
				elif choices[choicecode]['Requirements'][choicereq]['type'] == 'equip' :
					evaluator = choices[choicecode]['Requirements'][choicereq]['evaluator']
					id = int(choices[choicecode]['Requirements'][choicereq]['id'])
					if (id in equipment) != eval(evaluator) :
						reqpass = 0
				if reqpass == 0 :
					choicecodelist.remove(choicecode)
					break
		choicetextlist = []
		choicetextlist_lc = []
		opt = 0
		for element in choicecodelist :
			opt = opt+1
			achoicedesc = choices[element]['description']
			choicetext = str(opt)+") "+achoicedesc
			choicetextlist.append(choicetext)
			choicetextlist_lc.append(achoicedesc.lower())
		print '\n'.join(choicetextlist)
	scenechanged = 0
	while scenechanged == 0 : #The second stage loop. This is only left, and the code above run when the scene or scene state changes
		prompt = raw_input(">").lower() #The main prompt!
		clr()
		if prompt == "" :
			pass #If user presses enter without typing anything, do nothing
		else :
			splitprompt = prompt.split(' ',1)
			promptcomm = splitprompt[0]
			if len(splitprompt) > 1 :
				promptval = splitprompt[1]
			else :
				promptval = '-'
			
			if prompt in choicetextlist_lc :
				for position, item in enumerate(choicetextlist_lc):
					if item == prompt:
						chosen = choicecodelist[position]
				choiceeffects = choices[chosen]['Effects'].keys()
				for effectno in choiceeffects :
					seffectno = str(effectno)
					id = choices[chosen]['Effects'][seffectno]['id']
					usetype = choices[chosen]['Effects'][seffectno]['type']
					if usetype != 'equip' and usetype != 'scene' : value = choices[chosen]['Effects'][seffectno]['value']
					if usetype == 'vital' :
						operator = choices[chosen]['Effects'][seffectno]['operator']
						exec("character['Vitals'][id]"+operator+str(value))					
						statchanged = 1
					elif (usetype == 'vitalrestore') and (character['Vitals'][id] < character['Vitals']['Initial Values'][id]):
						exec("character['Vitals'][id]+="+str(value))
						if character['Vitals'][id] > character['Vitals']['Initial Values'][id] : character['Vitals'][id] = character['Vitals']['Initial Values'][id] 
						statchanged = 1
					elif usetype == 'attribute' :
						operator = choices[chosen]['Effects'][seffectno]['operator']
						exec("character['Attributes'][id]"+operator+str(value))
						statchanged = 1
					elif (usetype == 'attributerestore') and (character['Attributes'][id] < character['Attributes']['Initial Values'][id]) :
						exec("character['Attributes'][id]+="+str(value))
						if character['Attributes'][id] > character['Attributes']['Initial Values'][id] : character['Attributes'][id] = character['Attributes']['Initial Values'][id] 
						statchanged = 1
					elif usetype == 'additem' :
						for _ in repeat(None, value) :
							inventory.append(int(id))
						invchanged = 1
					elif usetype == 'equip' :
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
					elif usetype == 'scene' :
						scene.id = id		
				
			elif ((prompt == "choices" or prompt == "c") and choices != 0) or (prompt == "scene") or (prompt == "s" and (attributes == 0 and vitals == 0)) :
				print scene.description()
				if choices != 0 :
					print '\n'.join(choicetextlist) #Re-print scene choices
			
			elif (prompt == "status" or prompt == "s" or prompt == "health") and (attributes != 0 or vitals != 0):
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
								clr()
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
					clr()
					print "No items you possess can be used in that way\n" #Will soft-code
					useditem = 0
				else :
					potentialitems = []
					for element in tempinventory :
						if (promptval == items[str(element)]['description'].lower()) or (promptval in items[str(element)]['altdescs']) :
							potentialitems.append(element)
					if len(potentialitems) == 0 :
						clr()
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
								clr()
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
					clr()
					print "None of the listed items match that exact description"
				if reqpass == 1 :
					clr()
					print items[useditem]['Actions'][promptcomm]['Details']['text']
					if items[useditem]['Actions'][promptcomm]['Details']['singleuse'] == 1 :
						inventory.remove(int(useditem))
						invchanged = 1
					itemeffects = items[useditem]['Actions'][promptcomm]['Effects'].keys()
					for effectno in itemeffects :
						seffectno = str(effectno)
						id = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['id']
						usetype = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['type']
						if usetype != 'equip' and usetype != 'scene' : value = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['value']
						if usetype == 'vital' :
							operator = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['operator']
							exec("character['Vitals'][id]"+operator+str(value))					
							statchanged = 1
						elif (usetype == 'vitalrestore') and (character['Vitals'][id] < character['Vitals']['Initial Values'][id]):
							exec("character['Vitals'][id]+="+str(value))
							if character['Vitals'][id] > character['Vitals']['Initial Values'][id] : character['Vitals'][id] = character['Vitals']['Initial Values'][id] 
							statchanged = 1
						elif usetype == 'attribute' :
							operator = items[useditem]['Actions'][promptcomm]['Effects'][seffectno]['operator']
							exec("character['Attributes'][id]"+operator+str(value))
							statchanged = 1
						elif (usetype == 'attributerestore') and (character['Attributes'][id] < character['Attributes']['Initial Values'][id]) :
							exec("character['Attributes'][id]+="+str(value))
							if character['Attributes'][id] > character['Attributes']['Initial Values'][id] : character['Attributes'][id] = character['Attributes']['Initial Values'][id] 
							statchanged = 1
						elif usetype == 'additem' :
							for _ in repeat(None, value) :
								inventory.append(int(id))
							invchanged = 1
						elif usetype == 'equip' :
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
						elif usetype == 'scene' :
							scene.id = id
				elif reqpass == 0 :
					print items[useditem]['Actions'][promptcomm]['Requirements'][sreqno]['failtext']
			
			elif (prompt == "help") or (prompt == "h") or (prompt == "man") :
				print "Command List"
				print "'choices': review availible options"
				print "'inventory': view your inventory"
				print "'equipment': view what items you have equipped"
				print "'use #': Use or equip item with the number #"
				print "'status': view the statuses of your vitals and attributes"
				print "'about': show information about the adventure you are playing"
				print "'help': view these commands again"
				print "'quit': shut down the game engine"
			
			elif (prompt == "about") or (prompt == "credits") or (prompt == "a"):
				print "\n"+adventure.title+" was made by "+author
				print website
				print "You are currently on scene "+scene
			
			elif (prompt == "quit") or (prompt == "exit") or (prompt == "x") or (prompt == "leave") :
				print "Are you sure you want to quit?"
				answer = bool(yesno())				
				if answer == True :
					exit(0)
			
			elif promptcomm in main['Commands']['Items']['using'].keys() or promptcomm in promptcomm in main['Commands']['Items']['equipping'].keys():
				if promptval.isdigit() :
					print "'%s' should be followed by all or part of the description of an item - not a number" %(promptcomm)
				else :
					print "'%s' should be followed by all or part of the description of an item" %(promptcomm)
			else :
				print main['Messages']['unknowncommand']
			
			if (scene.id != character['Basics']['scene']) or (scene.state.id != scene.state.id_old) or (invchanged == 1) or (statchanged == 1) or (equipchanged == 1):
				character.write()
				if (scene.id != character['Basics']['scene']) or (scene.state.id != scene.state.id_old) :
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