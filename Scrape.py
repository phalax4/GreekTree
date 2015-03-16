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
		#print type(soup)
		print "Connection Success"
	def extract12Gods(self):
		objlist = []
		for td in self.tables[0]:
			soupa = BeautifulSoup(unicode(td))	
			#list12 =  soupa.findAll("b")
			#print soupa.findAll("a")
		  	for i in (soupa.select("td > b > a")):
		    		#print(i.get('href'))
		    		#print(i.get('title'))
		    		#print i
		    		link = self.mainUrl + i.get('href')
		    		#print link
		    		name = i.get('title')
		    		god = Deity(name,link)
		    		god.generation ="Olympian"
		    		god.typie = "Olympian"
		    		objlist.append(god)
			print(soupa.select("p"))
			#print "------------------------"
		return objlist  #returns list of 12 Olympian gods to main

#	def twelveGod(self):
	def extractWikiTables(self):
		print self.tables[1]	

if __name__=='__main__':#testing purposes
	scraper = Scrape()
	testList1 = scraper.extract12Gods()
	for i in testList1:
		print i.getName()