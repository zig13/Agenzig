class Equipment :
	def __init__(self, path, equiplist=[]) :
		self.list = []
		from configobj import ConfigObj
		self.file = ConfigObj(path.equipment, unrepr=True)
		self.file_slots = ConfigObj(path.equipslots, unrepr=True)
		self.dictionary = {}
		for slotx in self.file_slots.keys() :
			if self.file_slots[slotx]['type'] == 'natural' :
				self.equipment[slotx] = 0
		for equipx in self.list :
			self.equip(equipx)			
		
	def equip(self, id) :
		from functions import valremove, dupremove
		replacelists = {}
		replacetotals = {}
		equipx = self.file[id]
		for slotoptionx in equipx['Slots'].keys() :
			replaceditems = []
			for slotx in equipx['Slots'][slotoptionx] :
				try :
					if self.dictionary[slotx] != 0 :
						replaceditems.append(self.dictionary[slotx])
				except KeyError:
					return False
					break
			replaceditems = dupremove(valremove(replaceditems, 0))
			replacelists[slotoptionx] = replaceditems
			replacetotals[slotoptionx] = len(replaceditems)
		
		bestslotoption = min(replacetotals, key=replacetotals.get)
		replaceditems = replacelists[bestslotoption]
		for replacedx in replaceditems :
			self.unequip(replacedx)
		
		usedslots = equipx['Slots'][bestslotoption]
		for slotx in usedslots :
			self.dictionary[slotx] = id
			
		self.list.append(equipx)
			
		for effectx in equipx['Effects'].keys() :
		
		for actionx in equipx['Actions'].keys() :
			