import json
from Deity import *
from Link import *


class JSON_data:
	def __init__(self, nodes, links):
		self.nodes = nodes
		self.links = links

class Write_JSON:
	def __init__(self, obj):
		self.obj = obj

	def write(self):
		obj = json.dumps(self.obj,default=jdefault,indent=4,separators = (',',':'))
		with open('data.json', 'a') as f:
			f.write(obj)

# allows Python lists to be JSON encoded
def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

if __name__=='__main__':
	scraper = Scrape()
	objlist = []
	for i in [0,2]:
		objlist += scraper.extractWikiTables(i)
	m = MakeLinks(objlist)
	m.makeLinks()

	s = JSON_data(objlist, m.linklist)
	writer = Write_JSON(s)
	writer.write()