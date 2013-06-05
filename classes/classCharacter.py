class Character :
	alive = True
	def __init__(self, path, name) :
		self.path = path.charfolder+name
		from configobj import ConfigObj
		self.file = ConfigObj(self.path, unrepr=True)
		print self.path
		self.name = self.file['Basics']['charname']
		
	def set_equipment(self, path) :
		from classes.classEquipment import Equipment
		self.equipment = Equipment(path, self.file['Items']['Equipment'])
		
	def set_inventory(self, path) :
		from classes.classInventory import Inventory
		self.inventory = Inventory(path, self.file['Items']['Inventory'])
	
	def getscene(self) :
		return self.file['Basics']['scene']
		
	def checkstate(self, scene_id) :
		if scene_id in self.file['Scene States'].keys() : #If character file has noted the scenestate of the current scene to be different from default
			return self.file['Scene States'][scene.id]
		else :
			return '1'
	
	def rendertemp(self, list=None) :
		print stuff
	
	
	def renderperm(self, list=None) :
		print stuff
			
