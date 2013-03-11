class Scene:
	def __init__(self, path, scene_id) :
		self.path = path.scenes
		self.id = scene_id
		from configobj import ConfigObj
		self.file = ConfigObj(self.path, unrepr=True)		
		
	def setstate(self, state_id) :
		from classes.classSceneState import SceneState
		self.state = SceneState(state_id)
		
	def description(self) :
		return self.file[self.id][self.state.id]['description']
		
	def choices(self) :
		return self.file[self.id][self.state.id]['choices']