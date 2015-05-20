import json
from Deity import *
from Link import *
from Scrape import Scrape
import time
import multiprocessing as mp
class JSON_data:
	def __init__(self, nodes, links):
		self.nodes = nodes
		self.links = links

class Write_JSON:
	def __init__(self, obj):
		self.obj = obj

	def write(self):
		obj = json.dumps(self.obj,default=jdefault,indent=4,separators = (',',':'))
		with open('d3/data.json', 'w') as f:
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
	
	objlist2 = []
	output = mp.Manager().list()
	processes = []
	#for i in [0,1,2]:
	#	processes.append(mp.Process(target=scraper.extractWikiTables,args=(i,)))
	#processes = [mp.Process(target=scraper.extractWikiTables,args=(k,objlist)) for k in range(3)]
	for i in [0,1,2]:
		p = mp.Process(target=scraper.extractWikiTables,args=(i,output))
		processes.append(p)
		p.start()
	for p in processes:
		p.join()
	print output
	print len(output)
	t1 = time.time()

	t2 = time.time()
	output2 = mp.Manager().list()

	processes1 = [mp.Process(target=scraper.extractWikiLists,args=(i,output2)) for i in range(7)]
	for p in processes1:
		p.start()
	for p in processes1:
		p.join()
	#print len(output2)
	#print len(list(output)+list(output2))
	objlist = (list(output)+list(output2))
	t3 = time.time()

	print "WikiTables, takes %f seconds"%(t1-t0)

	print "WikiLists takes %f seconds"%(t3-t2)
	#for i in objlist:
	#	for j in objlist:
	newlist = []
	for i in objlist:
		if i not in newlist:
			newlist.append(i)
			#print i.name
	objlist = newlist
	for i in newlist:
		print i.name
	t8 = time.time()
	m = MakeLinks(newlist)
	m.makeLinks()
	t9 = time.time()
	print "Making links takes: %f"%(t9 - t8)

	t10 = time.time()
	s = JSON_data(newlist, m.linklist)
	writer = Write_JSON(s)
	writer.write()
	t11 = time.time()
	print "Writing to file takes: %f"%(t11 - t10)
