import json
from Deity import *
from Link import *
from Scrape import Scrape
import time

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
	t0 = time.time()
	tlist1 = []
	tlist2 = []
	for i in [0,1,2]:
		t2 = time.time()
		scraper.extractWikiTables(i,objlist)
		t3 = time.time()
		tlist1.append(t3-t2)
		#print "WikiTable: %f, takes %f"%(i,(t3-t2))
	t1 = time.time()
	t4 = time.time()
	for i in list(range(7)):
		t6 = time.time()
		scraper.extractWikiLists(i,objlist)
		t7 = time.time()
		tlist2.append(t7-t6)
		#print "WikiList: %f, takes %f"%(i,(t7-t6))
	t5 = time.time()
	c = 0
	for i in tlist1:
		print "WikiTable: %d, takes %f seconds"%(c,i)
		c = c+1
	c = 0
	for i in tlist1:
		print "WikiLists: %d, takes %f seconds"%(c,i)
		c = c+1
	print "WikiTables takes: %f" % (t1-t0)
	print "WikiLists takes: %f" %(t5 - t4)

	for i in objlist:
		pass
	t8 = time.time()
	m = MakeLinks(objlist)
	m.makeLinks()
	t9 = time.time()
	print "Making links takes: %f"%(t9 - t8)

	t10 = time.time()
	s = JSON_data(objlist, m.linklist)
	writer = Write_JSON(s)
	writer.write()
	t11 = time.time()
	print "Writing to file takes: %f"%(t11 - t10)
