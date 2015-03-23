#!/usr/bin/python
import json
class Deity:
	def to_JSON(self):
		return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)#+ ",\n"
	def __init__(self,name,link):
		self.name = name
		self.link = link
		self.group = -1
		self.parents = []
		self.siblings = []
		self.children = []
		self.sub = []
	typie = ""
	attribute = ""

	def getName(self):
		return self.name
	def __eq__(self, other): #for searching through the list
		return self.link == other.link

if __name__=='__main__':#testing purposes
	testGod = Deity("Fyodor Pavlovich Karamazov", "http//:Russia")
	testGod.group = 1
	testGod.typie = "Sensualist"
	testGod.attribute = "Money"
	print testGod.to_JSON()
	testGod2 = Deity("Alexei Fydorovich Karamazov","http//:Russia")
	testGod.group = 2
	testGod.typie = "Faithful"
	testGod.attribute = "Religion"
	objlist = [testGod,testGod2]

