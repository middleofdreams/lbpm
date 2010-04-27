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
		if BS:
			

			self.timer.start(1)
			self.timer.setInterval(400)
			try:
				sock = urllib.urlopen(self.url)
			except:
				self.title=""
				self.timer.stop()
				self.end()
				self.stop()
			
			try:
				htmlSource = BeautifulSoup(sock.read())
				sock.close()
			except:
				htmlSource = BeautifulSoup("<title> </title>")
			
		
		
			try:
				self.title=htmlSource.find('title').contents[0].strip()
			except:
				self.title=""
			try:
				self.unescape()
			except: pass
			self.end()
		else:
			guihelpers.message(self.tr("Error"),self.tr("You need to install BeautifulSoup for that!"),True)
	
		
		
	def unescape(self):
		self.title= re.sub('&(%s);' % '|'.join(name2codepoint), 
				lambda m: unichr(name2codepoint[m.group(1)]), self.title)

	
	def end(self):
		self.timer.setInterval(0)
		self.timer.stop()
		pass

