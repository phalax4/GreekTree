#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup, NavigableString
from Deity import *
class Scrape:
	def __init__(self):
		self.url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures")
		self.content = self.url.read()
		self.soup =  BeautifulSoup(self.content)
		self.tables = [] #table holder for 3 wikitables
		self.lists = []
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
			a = soupb.find("a")
			if x == 0:
				b = soupb.find("b")
				if b: a = b.find("a")
			if a:
				link = self.mainUrl + a.get('href')
				name = a.get('title')
				if name.find("(")!= -1: #parse out (mythology) substring
					name = name[0:name.index("(")]
				god = Deity(name,link)
				if x == 0:
					group = 2
					ty = "Immortal"
				elif x == 1:
					group = 0
					ty = "Primeval"
				elif x == 2:
					group = 1
					ty = "Immortal"
				else:
					group = -1
					ty = ""
				god.group = group
				god.typie = ty
				s = ScrapeDeity(god, god.link)
				s.extractInfobox()
				if god not in objlist:
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
				#s = ScrapeDeity(god, god.link)
				#s.extractInfobox()
				objlist.append(god)

				ull = i.find("ul")
				if ull:
					for s in ull.find_all("li",recursive=False):
						suba = s.find("a", recursive=False)
						if suba != None:
							subname = suba.text.encode('utf-8')
						else:
							subname = s.text.encode('utf-8').split(" ")[0]
						god.sub += [subname]
		return objlist

class ScrapeDeity:
	def __init__(self, deity, link):
		self.url = urllib2.urlopen(link)
		self.content = self.url.read()
		self.soup = BeautifulSoup(self.content)
		self.deity = deity

	@staticmethod
	def isWord(x):
		if len(x) >= 1:
			if (ord(x[0]) >= 64 and ord(x[0]) <= 90) or (ord(x[0]) >= 97 and ord(x[0]) <= 122): 
				if ("and" not in x) and ("the" not in x) and ("None" not in x):
					return True
		return False

	def extractInfobox(self):
		infobox = self.soup.find("table", {"class" : "infobox"})
		if infobox:
			for tr in infobox.select("tr"):
				th = tr.find("th")
				if th:
					category = th.text.encode('utf-8')
					if category == "Children":
						td = tr.find("td")
						for thing in td.children:
							if type(thing) == NavigableString:
								lst = thing.split(", ")
								self.deity.children += [x for x in lst if self.isWord(x)]
							else:
								if self.isWord(thing.text):
									self.deity.children += [thing.text]

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
