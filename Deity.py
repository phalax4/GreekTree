#!/usr/bin/python
import json
class Deity:
	def to_JSON(self):
		return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)
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
		obj = self.deity.to_JSON()
		f = open('data.json', 'a')
		with open('data.json', 'a') as f:
			f.write(obj)
