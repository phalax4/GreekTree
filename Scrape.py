#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from Deity import Deity
class Scrape:
	def __init__(self):
		self.url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures")
		self.content = self.url.read()
		self.soup =  BeautifulSoup(self.content)
		self.tables = [] #table holder for 3 wikitables
		self.mainUrl = "http://en.wikipedia.org"  #Seems like everything has this as prefix for link
		#### Add more attributes for other "segements" of the page
		self.connect() #connects to the list of myth figures web page
	def connect(self):		
		url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures")
		content = url.read()
		soup = BeautifulSoup(content)  #soup contains the Object to access page
		self.tables = self.soup.findAll("table", {"class" : "wikitable"}) #Grabs the 3 wiki tables: Titans, 12 Gods and Primordial
		self.lists = self.soup.findAll("div", {"class": "div-col columns column-count column-count-"})
		#print type(soup)
		print "Connection Success"
	def extractWikiTables(self,x): #specify which wiki table to get
		objlist = []
		#print self.tables[]
		for td in self.tables[x]:
			soupb = BeautifulSoup(unicode(td))
			searching = "td > a"
			if x == 0:
				searching = "td > b > a"
			for i in (soupb.select(searching)):
				link = self.mainUrl + i.get('href')
				name = i.get('title')
				if name.find("(")!= -1: #parse out (mythology) substring
					name = name[0:name.index("(")]
				#print name
				god = Deity(name,link)
				ty = ""
				if x == 0:
					gen = 2
					ty = "Immortal"
				elif x == 1:
					gen = 0
					ty = "Primeval"
				elif x == 2:
					gen = 1
					ty = "Immortal"
				else:
					gen = -1
				god.group = gen
				god.typie = ty
				objlist.append(god)
			#list2 = (soupb.select("td"))
			#if(len(list2)>0):     ######Grabs the paragraph blurb
			#	print list2[2]
		return objlist
	
	def createDeityObject(self, i, a):
		if a != None:
			link = self.mainUrl + a.get('href')
			name = a.text.encode('utf-8')
		else: #if there is no link
			link = ""
			name = i.text.encode('utf-8').split(" ")[0]
		god = Deity(name,link)
		return god
	
	def extractWikiLists(self, x): #getting names of giants and personified concepts
		objlist = []
		soupb = BeautifulSoup(unicode(self.lists[x]))
		for ul in soupb.find("div").find_all("ul",recursive=False):
			for i in (ul.find_all("li", recursive=False)):
				a = i.find("a")
				god = self.createDeityObject(i, a)
				gen = -1
				ty = ""
				if x == 0:
					ty = "Giant"
				elif x == 1:
					ty = "Spirit"
				god.group = gen
				god.typie = ty
				objlist.append(god)

				ull = i.find("ul")
				if ull:
					for s in ull.find_all("li",recursive=False):
						subgod = self.createDeityObject(s, s.find("a"))
						subgod.group = god.group
						subgod.typie = "something"
						god.sub += [subgod]
		return objlist

if __name__=='__main__':#testing purposes
	scraper = Scrape()
	#testList1 = scraper.extract12Gods()
	lis = [0,1,2]
	for i in lis:
		testList1 = scraper.extractWikiTables(i)
		for i in testList1:
			print i.getName() + " " + i.group
	for i in [0,1]:
		testList2 = scraper.extractWikiLists(i)
		for i in testList2:
			print i.getName() + " " + i.typie
