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

	def makeLinks(self): #links for children
		for i in range(len(self.objlist)):
			deity = self.objlist[i]
			for child in deity.children:
				for j in range(len(self.objlist)):
					if self.objlist[j].name == child:
						target = j
						link = Link(i, target, 1)
						link.parent = deity.name
						link.child = child
						self.linklist += [link]
						break


