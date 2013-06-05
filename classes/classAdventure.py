class Adventure :	
	def __init__(self, foldername) :
		from classes.classPath import Path
		self.path = Path(foldername)
	def validate(self) :
		from os import access, R_OK
		if not access(self.path.advfile['Main'], R_OK) : raise validation_fail("Main file missing")
		from configobj import ConfigObj
		self.file = ConfigObj(self.path.advfile['Main'], unrepr=True)
		reqfiles = self.path.datafiles(self.file['Details']['required_data_files'])
		for fileindex in reqfiles :
			if not access(self.path.advfile[fileindex], R_OK) : raise validation_fail(self.path.filenames[fileindex]+" file missing")
		
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