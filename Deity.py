#!/usr/bin/python
import json
class Deity:
	def to_JSON(self):
		return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)
	def write_JSON(self):
		obj = self.to_JSON() + ",\n"
		with open('data.json', 'a') as f:
			f.write(obj)
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


