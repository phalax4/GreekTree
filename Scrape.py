#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup, NavigableString
from Deity import *
class Scrape:
	def __init__(self):
		self.url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures") #open initial link
		self.content = self.url.read()
		self.soup =  BeautifulSoup(self.content)
		self.tables = [] #table holder for 3 wikitables
		self.lists = []
		self.mainUrl = "http://en.wikipedia.org"  #Seems like everything has this as prefix for link
		#### Add more attributes for other "segements" of the page
		self.connect() #connects to the list of myth figures web page
	def connect(self):		
		url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures")
		content = self.url.read()
		soup = BeautifulSoup(content)  #soup contains the Object to access page
		self.tables = self.soup.findAll("table", {"class" : "wikitable"}) #Grabs the 3 wiki tables: Titans, 12 Gods and Primordial
		self.lists = self.soup.findAll("div", {"class": "div-col columns column-count column-count-"})
		#print type(soup)
		print "Connection Success"
		
	def find(self, name, objlist):
		for god in objlist:
			if str(god.name) == name:
				return True
		return False

	def extractWikiTables(self,x,objlist): #specify which wiki table to get
		#print self.tables[]
		for td in self.tables[x]:
			soupb = BeautifulSoup(unicode(td))
			list2 = (soupb.select("p"))
			list3 = (soupb.select("td"))
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
					ty = "Immortal"
				elif x == 1:
					ty = "Primeval"
				elif x == 2:
					group = 1
					ty = "Immortal"
				else:
					ty = ""
				god.typie = ty
				attribute = ""
				if(len(list3)==3):     ######Grabs the paragraph blurb for titan and primordial
					#print list3[2]
					string = (str((list3[2]))[4:])
					attribute = string[:string.find(".")+1]
					print attribute
					#print string[:string.find(".")+1]
					#print list3[2]
				elif(len(list3)==2):  ###Paragraph for the 12 main deities
					string = (str((list2[0]))[3:])
					attribute = string[:string.find(".")+1]
					print attribute
					#print string[:string.find(".")+1]#[soupb.extract() for i in list2]
				else:
					attribute = "NULL"
				god.attribute = attribute
				#checking if it is already in the list
				if not self.find(god.name, objlist):
					#going into the deity's webpage
					if god.link:
						s = ScrapeDeity(god, god.link)
						print god.link
						s.extractInfobox()
					objlist.append(god)				
	#returns a deity object given soup.find("li") and soup.find("a")			
	def createDeityObject(self, li, a):
		if a != None:
			link = self.mainUrl + a.get('href')
			name = a.text.encode('utf-8')
		else: #if there is no link
			link = ""
			name = li.text.encode('utf-8').split(" ")[0]
			if name.find(",")!= -1: #parse out (mythology) substring
					name = name[0:(name.index(",")-1)]
		god = Deity(name,link)
		return god
	
	def extractWikiLists(self, x, objlist): #getting names of all other deities
		soupb = BeautifulSoup(unicode(self.lists[x]))
		for ul in soupb.find("div").find_all("ul",recursive=False):
			for li in (ul.find_all("li")):
				a = li.find("a", recursive=False)
				god = self.createDeityObject(li, a)
				ty = ""
				if x == 0:
					ty = "Giant"
				elif x == 1:
					ty = "Spirit"
				god.typie = ty
				
				if not self.find(god.name, objlist):
					#going into the deity's webpage:
					if god.link and god.link != "":
						#print god.link
						string = god.link
						s = ScrapeDeity(god,string)
						print god.link
						s.extractInfobox()
					objlist.append(god)
				
				"""
				#gets deities in a subcategory
				ull = li.find("ul")
				if ull:
					for s in ull.find_all("li",recursive=False):
						suba = s.find("a", recursive=False)
						if suba != None:
							subname = suba.text.encode('utf-8')
						else:
							subname = s.text.encode('utf-8').split(" ")[0]
						god.sub += [subname]
				"""

class ScrapeDeity:
	def __init__(self, deity, link):
		self.url = urllib2.urlopen(link)#open link into child page
		self.content = self.url.read()
		self.soup = BeautifulSoup(self.content)
		self.deity = deity

	@staticmethod
	#checks if something in a list is an actual word -- should be improved
	def isWord(x):
		if len(x) >= 1:
			if (ord(x[0]) >= 64 and ord(x[0]) <= 90) or (ord(x[0]) >= 97 and ord(x[0]) <= 122): 
				if ("and " not in x) and ("the " not in x) and (" the" not in x) and (" or" not in x) and ("None" not in x):
					return True
		return False

	# adds the list of names/objects in an infobox category to a Deity object
	def extractInfoboxList(self, tr, attribute):
		td = tr.find("td")
		for thing in td.children:
			if type(thing) == NavigableString:
				lst = thing.split(", ")
				self.deity.__dict__[attribute] += [x for x in lst if self.isWord(x)]
			else:
				text = thing.text.encode('utf-8')
				if self.isWord(text):
					self.deity.__dict__[attribute] += [text]
	
	# searches through infobox
	def extractInfobox(self):
		infobox = self.soup.find("table", {"class" : "infobox"})
		if infobox:
			for tr in infobox.select("tr"):
				th = tr.find("th")
				if th:
					category = th.text.encode('utf-8')
					if category == "Children":
						self.extractInfoboxList(tr, "children")
					if category == "Parents":
						self.extractInfoboxList(tr, "parents")
		else:
			return -1;

if __name__=='__main__':#testing purposes
	scraper = Scrape()
	#testList1 = scraper.extract12Gods()
	lis = [0,1,2]
	objlist = []
	for i in lis:
		testList1 = scraper.extractWikiTables(i,objlist)
		for i in testList1:
			print i.getName() + " " + i.group
	for i in [0,1]:
		testList2 = scraper.extractWikiLists(i)
		for i in testList2:
			print i.getName() + " " + i.typie
