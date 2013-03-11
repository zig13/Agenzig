class Adventure :	
	def __init__(self, foldername) :
		from classes.classPath import Path
		self.path = Path(foldername)
	def validate(self) :
		from os import access, R_OK
		if not access(self.path.main, R_OK) : raise validation_fail("Main file missing")
		if not access(self.path.scenes, R_OK) : raise validation_fail("Scenes file missing")
		from configobj import ConfigObj
		self.file = ConfigObj(self.path.main, unrepr=True)
		self.requirements = self.file['Details']['requirements']
		self.path.reqfiles(self.requirements)
		if self.requirements[0] == 1 and not access(self.path.abilities, R_OK) : raise validation_fail("abilities file missing")
		if self.requirements[1] == 1 and not access(self.path.attributes, R_OK) : raise validation_fail("attributes file missing")
		if self.requirements[2] == 1 and not access(self.path.cabilities, R_OK) : raise validation_fail("cabilities file missing")
		if self.requirements[3] == 1 and not access(self.path.categories, R_OK) : raise validation_fail("categories file missing")
		if self.requirements[4] == 1 and not access(self.path.choices, R_OK) : raise validation_fail("choices file missing")
		if self.requirements[5] == 1 and not access(self.path.confrontations, R_OK) : raise validation_fail("confrontations file missing")
		if self.requirements[6] == 1 and not access(self.path.equipment, R_OK) : raise validation_fail("equipment file missing")
		if self.requirements[7] == 1 and not access(self.path.equipslots, R_OK) : raise validation_fail("equipslots file missing")
		if self.requirements[8] == 1 and not access(self.path.items, R_OK) : raise validation_fail("items file missing")
		if self.requirements[9] == 1 and not access(self.path.vitals, R_OK) : raise validation_fail("vitals file missing")
		
	def details(self) :
		self.title = self.file['Details']['title']
		self.blurb = self.file['Details']['blurb']
		self.author = self.file['Details']['author']
		self.website = self.file['Details']['website']
		self.charcreator = self.file['Details']['charcreator']

class validation_fail(Exception):
	def __init__(self, reason=""):
		self.reason = reason
	def __str__(self):
		return repr(self.reason)