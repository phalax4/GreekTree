#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from Deity import Deity
class Scrape:
	def __init__(self):
		self.url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures")
		self.content = self.url.read()
		self.soup =  BeautifulSoup(self.content)
		self.tables = []
		self.mainUrl = "http://en.wikipedia.org"
		self.connect()
	def connect(self):		
		url = urllib2.urlopen("http://en.wikipedia.org/wiki/List_of_Greek_mythological_figures")
		content = url.read()
		soup = BeautifulSoup(content)
		self.tables = self.soup.findAll("table", {"class" : "wikitable"})

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
		    		print i
		    		link = self.mainUrl + i.get('href')
		    		#print link
		    		name = i.get('title')
		    		god = Deity(name,link)
		    		god.generation ="Olympian"
		    		god.typie = "Olympian"
		    		objlist.append(god)
			soupa1 = BeautifulSoup(unicode(soupa.findAll('p')))
			
			print "------------------------"
		return objlist

#	def twelveGod(self):
	def extractWikiTables(self):
		print self.tables[0]	


