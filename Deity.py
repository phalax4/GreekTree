#!/usr/bin/python
import json
class Deity:
	def to_JSON(self):
		return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)#+ ",\n"
	def __init__(self,name,link):
		self.name = name
		self.link = link
	generation = ""
	typie = ""
	attribute = ""
	parent = []
	siblings = []
	children = []
	def getName(self):
		return self.name
class Write_JSON:
	def __init__(self, deity):
		self.deity = deity
	def write(self):
		obj = self.deity#.to_JSON()
		with open('data.json', 'a') as f:
			f.write(obj)

if __name__=='__main__':#testing purposes
	testGod = Deity("Fyodor Pavlovich Karamazov", "http//:Russia")
	testGod.generation = 1
	testGod.typie = "Sensualist"
	testGod.attribute = "Money"
	print testGod.to_JSON()
	testGod2 = Deity("Alexei Fydorovich Karamazov","http//:Russia")
	testGod.generation = 2
	testGod.typie = "Faithful"
	testGod.attribute = "Religion"
	objlist = [testGod,testGod2]
	s = json.dumps([g.__dict__ for g in objlist],indent=4,separators = (',',':'))
	print s
	writer = Write_JSON(s)
	writer.write()
	#for i in objlist:
	#	writer = Write_JSON(i)
	#	writer.write()


