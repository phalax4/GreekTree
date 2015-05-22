import urllib2
from bs4 import BeautifulSoup, NavigableString
from Deity import *
from nltk import word_tokenize

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
		print "Connection Success"
		
	def find(self, name, objlist):
		for god in objlist:
			if str(god.name) == name:
				return True
		return False

	def extractWikiTables(self,x,objlist): #specify which wiki table to get
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
					name = name[0:(name.index("(")-1)]
				god = Deity(name,link)
				ty = ""
				attr = ""	
				if x == 0:
					ty = "Immortal"
				elif x == 1:
					ty = "Primeval"
				elif x == 2:
					ty = "Immortal"
					attr = "Titan"		

				god.typie = ty
				god.attribute = attr

				if not self.find(god.name, objlist):
					if god.link: #going into the deity's webpage
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
	
	def extractWikiLists(self, x, objlist): #getting names from lists
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

				#finding subgods
				ull = li.find("ul")
				if ull:
					for s in ull.find_all("li",recursive=False):
						suba = s.find("a", recursive=False)
						if suba != None:
							subname = suba.text.encode('utf-8')
						else:
							subname = s.text.encode('utf-8').split(" ")[0]
						god.sub += [subname]	

				if not self.find(god.name, objlist):
					#going into the deity's webpage:
					if god.link:
						s = ScrapeDeity(god, god.link)
						print god.link
						ifInfobox = s.extractInfobox()
						if ifInfobox == -1:
							s.extractFromParagraph()
					objlist.append(god)			

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
				if ("and " not in x) and ("the " not in x) and (" the" not in x) and (" or" not in x) and (" or" not in x) and (x != "or") and ("None" not in x):
					return True
		return False
	
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
					if text[:4] == "The ":
						text = text[4:]
					self.deity.__dict__[attribute] += [text]

	def extractFromParagraph(self):
		raw = self.soup.get_text()
		page = self.soup.find_all('p')
		for p in page:
			tokens = word_tokenize(p.text)
			for i in range(1, len(tokens)):
				phrase = tokens[i-1] + tokens[i]	#getting two adjacent words
				phrase = phrase.encode('utf-8')
				
				#getting parents of deity
				parentstrings = ['offspringof', 'sonof', 'sonsof', 'daughterof', 'daughtersof', 'motherwas', 'descendedfrom']
				j = i 	#counter for getting names
				if phrase in parentstrings:
					while j < len(tokens):	#loop through following words
						if tokens[j].istitle():		#names are capitalized
							#print "parent of: " + self.deity.name + " " +  tokens[j]
							self.deity.parents += [tokens[j]]	#add to the parents list
						if tokens[j] in '.;,':
							break	#end of sentence/phrase
						j += 1
			if self.deity.parents != []:
				break	#stop searching if things have been found
				
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
