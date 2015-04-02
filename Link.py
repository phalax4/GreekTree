from Deity import *

class Link:
	def __init__(self, source, target, value):
		self.source = source
		self.target = target
		self.value = value
	parent = ""
	child = ""

class MakeLinks:
	def __init__(self, objlist):
		self.objlist = objlist
		self.linklist = []
	
	def find(self, name):
		for i in range(len(self.objlist)):
			if self.objlist[i].name == name:
				return self.objlist[i]

	def makeLinks(self): #links for children
		#setting generation numbers
		first = self.find("Gaia")
		first.group = 0
		self.generations(first)
		
		for i in range(len(self.objlist)):
			deity = self.objlist[i]
			#links for children
			for child in deity.children:
				for j in range(len(self.objlist)):
					if str(self.objlist[j].name) == str(child):
						target = j
						link = Link(i, target, 1)
						self.linklist += [link]
						break
	def generations(self,deity):
		if deity.children != []:
			if "Titans" in deity.children:
			 	deity.children += ["Oceanus","Tethys","Hyperion","Theia","Coeus","Phoebe","Cronus","Rhea","Mnemosyne","Themis","Crius","Iapetus"]
			g = deity.group + 1
			for child in deity.children:
				for j in range(len(self.objlist)):
					if str(self.objlist[j].name) == str(child):
						newdeity = self.objlist[j]
						newdeity.group = g
						self.generations(newdeity)				
						break


