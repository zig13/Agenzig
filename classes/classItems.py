class Inventory :
	def __init__(self, path, inventory=[]) :
		self.list = []
		from configobj import ConfigObj
		self.file = ConfigObj(path.items, unrepr=True)
		self.dictionary = {}
		for itemx in self.list :
			self.additem(itemx)			
		
	def additem(self, id) :
		from functions import valremove, dupremove
		itemx = self.file[id]
		try :
			self.dictionary[itemx] += 1
		except KeyError:
			self.dictionary[itemx] = 1
		
		self.list.append(itemx)
			
		for effectx in itemx['Wffects'].keys() :
		
		
		
		for actionx in itemx['Actions'].keys() :
			