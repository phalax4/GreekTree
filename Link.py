from Scrape import *
from Deity import *

class Link:
	def __init__(self, source, target, value):
		self.source = source
		self.target = target
		self.value = value

class MakeLinks:
	def __init__(self, objlist):
		self.objlist = objlist
		self.linklist = []

	def find(self, name):
		for i in range(len(self.objlist)):
			if self.objlist[i].name == name:
				return self.objlist[i]

	def makeLinks(self): 
		#getting generation numbers
		#nyx = self.find("Nyx")
		#nyx.group = 0
		#self.generations(nyx)
		for i in range(len(self.objlist)):
			deity = self.objlist[i]
			#links for children
			for child in deity.children:
				for j in range(len(self.objlist)):
					if self.objlist[j].name == child:
						target = j
						link = Link(i, target, 1)
						self.linklist += [link]
						break
			#links for parents
			for parent in deity.parents:
				for j in range(len(self.objlist)):
					if self.objlist[j].name == parent:
						target = j
						link = Link(i, target, 1)
						self.linklist += [link]
						break
			#links for subcategories
			if deity.sub != []:
				deity.typie = "Category"
				for subgod in deity.sub:
					for j in range(len(self.objlist)):
						if self.objlist[j].name == subgod:
							target = j
							link = Link(i, target, 2)
							self.linklist += [link]
							break


	def generations(self,deity):
		if deity.children != []:
			if ("Titans" in deity.children) or ("The Titans" in deity.children):
				for god in self.objlist:
					if god.attribute == "Titan":
						deity.children += [god.name]
			if ("The Gigantes" in deity.children):
				for god in self.objlist:
					if god.attribute == "Gigante":
						deity.children += [god.name]

			g = deity.group + 1
			for child in deity.children:
				for j in range(len(self.objlist)):
					if self.objlist[j].name == child:
						newdeity = self.objlist[j]
						newdeity.group = g
						self.generations(newdeity)				
						break

