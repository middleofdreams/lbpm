# -*- coding: utf-8 -*-
import urllib,re,time,guihelpers
from htmlentitydefs import name2codepoint
from PyQt4 import QtCore,QtGui
try:
	from BeautifulSoup import BeautifulSoup
	BS=True
except:
	BS=False
	
class TitleLoader(QtCore.QThread):
	def __init__(self, url):
		super(TitleLoader, self).__init__(None)

		self.url=url
		self.timer=QtCore.QTimer()
	
	def run(self):
		global BS
		self.BS=BS
		self.timer.start(1)
		self.timer.setInterval(400)
		try:
			sock = urllib.urlopen(self.url)
		except:
			self.title=""
			self.timer.stop()
			self.end()
			self.stop()
		content=sock.read()
		sock.close()
		if BS:			
			if self.getTitleByBS(content)>0:
				self.getTitleManually(content)
		else:
			self.getTitleManually(content)
		sock.close()
		self.end()
		
	def getTitleByBS(self,content):
			err=0
			try:
				htmlSource = BeautifulSoup(content)	
			except:
				htmlSource = BeautifulSoup("<title> </title>")
				err=1
			self.title=htmlSource.find('title').contents[0].strip()
			
			try: self.unescape()
			except: pass
			return err
	
	def getTitleManually(self,content):
		content=content.lower().strip()
		idx1=content.find("<title>")
		idx2=content.find("</title>",idx1)
		self.title= content[idx1+len("<title>"):idx2].strip().capitalize()
		try: self.unescape()
		except: pass

		
		
	def unescape(self):
		self.title= re.sub('&(%s);' % '|'.join(name2codepoint), 
				lambda m: unichr(name2codepoint[m.group(1)]), self.title)

	
	def end(self):
		self.timer.setInterval(0)
		self.timer.stop()
		pass

