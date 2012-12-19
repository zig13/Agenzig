class Path :	
	def __init__(self, foldername=None) :
		from os import pardir, curdir, sep, listdir
		from os.path import abspath
		if foldername == None :
			self.advsfolder = curdir+sep+"Adventures"+sep
			self.adventures = listdir(self.advsfolder)
			self.advstotal = len(listdir(self.advsfolder))
		else :		
			self.folder = curdir+sep+"Adventures"+sep+foldername+sep
			self.charfolder = self.folder+"Characters"+sep
			self.main = self.folder+"Main.agez"
			self.scenes = self.folder+"scenes.agez"
		
	def validate(self, requirements=None) :
		from os import access, R_OK
		if not access(self.advsfolder, R_OK) : raise validation_fail("Adventures folder missing")
		if self.advstotal < 1 : raise validation_fail("No adventures installed")		
		
	def reqfiles(self, requirements) :
		if requirements[0] == 1 : self.abilities = self.folder+"abilities.agez"
		if requirements[1] == 1 : self.attributes = self.folder+"attributes.agez"
		if requirements[2] == 1 : self.cabilities = self.folder+"cabilities.agez"
		if requirements[3] == 1 : self.categories = self.folder+"categories.agez"
		if requirements[4] == 1 : self.choices = self.folder+"choices.agez"
		if requirements[5] == 1 : self.encounters = self.folder+"encounters.agez"
		if requirements[6] == 1 : self.equipment = self.folder+"equipment.agez"
		if requirements[7] == 1 : self.equipslots = self.folder+"equipslots.agez"
		if requirements[8] == 1 : self.items = self.folder+"items.agez"
		if requirements[9] == 1 : self.vitals = self.folder+"vitals.agez"
	
	def setchar(self, charname) :
		self.charfile = self.charfolder+charname
		return self.charfile
		
class validation_fail(Exception):
	def __init__(self, value=None):
		self.value = value
	def reason(self):
		return repr(self.value)
