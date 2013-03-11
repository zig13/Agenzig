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
		self.inventory = Inventory(path, self.file['Items'][Inventory'])
	
	def getscene(self) :
		return self.file['Basics']['scene']
		
	def checkstate(self, scene_id) :
		if scene_id in self.file['Scene States'].keys() : #If character file has noted the scenestate of the current scene to be different from default
			return self.file['Scene States'][scene.id]
		else :
			return '1'
	
	def item(self, item_id, action) :
		
	
	
	
	
	
	
	
	
	
	def equip(self, item_id, slotsused) :
		charequips = self.file['Items']['Equipment']
		replaceditems = []
		for slot in slotsused :
			if str(slotx) in .keys() : #If there is already a piece of equipment occupying the slot
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
