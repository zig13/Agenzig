#-------------------------------------------------------------------------------
# Name:        Agenzig Character Creator
# Purpose:     Character creator for a the text-based adventure game engine - Agenzig
#
# Author:      Thomas Sturges-Allard
#
# Created:     15/12/2012
# Copyright:   (c) Thomas Sturges-Allard 2011
# Licence:      Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#			http://creativecommons.org/licenses/by-nc-sa/3.0/
#-------------------------------------------------------------------------------
from classes.classPath import Path
path = Path()

if path.validate() == False :
	raw_input("No adventures are installed to create characters for.\nAdventures should be in individual folders inside a directory named 'Adventures' within this one.")
	exit(0)

from functions import Clr, yesno, choicelist
while True :
	success = False
	if path.advstotal == 1 :
		from classes.classAdventure import Adventure, validation_fail
		adventure = Adventure(path.adventures[0])
		try :
			adventure.validate()
		except validation_fail as e:
			print e.reason, "from adventure folder.\n"
			raw_input("Character creation cannot continue")
			exit(0)
	else :
		from classes.classAdventure import Adventures, Adventure, validation_fail
		print "Listing Adventures:"
		while True :
			print "Which adventure would you like to make a character for?"
			choice = choicelist(path.adventures)
			try :		
				adventure = Adventure(choice[1])
				adventure.validate()
				break
			except validation_fail as e:
				print e.reason, "\nPlease choose a different adventure\n"
	
	adventure.details()
	
	exec "from charcreators."+adventure.charcreator+" import createchar"
	success = bool(createchar(adventure.path))
	Clr()
	if success == True :
		print "Character created successfully\n"
	else :
		print "Character creation failed\n"
	print "Would you like to create another?"
	answer = bool(yesno())
	Clr()
	if answer == False :
		break
	

		