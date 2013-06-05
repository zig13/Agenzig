class Path :	
	filenames = ['abilities', 'actions', 'actions_encounter', 'attributes', 'categories', 'choices', 'classifications', 'currencies', 'encounters', 'equipment', 'equipment_slots', 'items', 'scenes', 'vitals']
	advfile = {}
	def __init__(self, foldername=None) :
		from os import pardir, curdir, sep, listdir
		from os.path import abspath
		if foldername == None :
			self.advsfolder = curdir+sep+"Adventures"+sep
			self.adventures = listdir(self.advsfolder)
			self.advstotal = len(self.adventures)
		else :		
			self.folder = curdir+sep+"Adventures"+sep+foldername+sep
			self.charfolder = self.folder+"Characters"+sep
			from os import access, R_OK
			if not access(self.charfolder, R_OK) : 
				from os import makedirs
				makedirs(self.charfolder)
			self.characters = listdir(self.charfolder)
			self.chartotal = len(self.characters)
			self.advfile['Main'] = self.folder+"Main.agez"
		
	def validate(self, requirements=None) :
		from os import access, R_OK
		if not access(self.advsfolder, R_OK) : raise validation_fail("Adventures folder missing")
		if self.advstotal < 1 : raise validation_fail("No adventures installed")		
		
	def datafiles(self, boolfiles) :
		reqfiles = []
		for index, reqbool in enumerate(reqfiles) :
			if reqbool == True : 
				self.advfile[self.filenames[index]] = (self.folder+self.filenames[index]+".agez")
				self.advfile[index] = (self.folder+self.filenames[index]+".agez")
				reqfiles.append(index)
		return reqfiles
	
	def setchar(self, charname) :
		self.charfile = self.charfolder+charname
		return self.charfile
		
class validation_fail(Exception):
	def __init__(self, value=None):
		self.value = value
	def reason(self):
		return repr(self.value)
