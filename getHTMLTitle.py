# -*- coding: utf-8 -*-
import urllib,codecs,re
from htmlentitydefs import name2codepoint
from PyQt4 import QtCore,QtGui

class TitleLoader(QtCore.QThread):
	def __init__(self, parent, url):
		super(TitleLoader, self).__init__(parent)
		self.ui = parent.ui
		self.parent = parent
		self.url=url
		self.running=False
		self.timer=QtCore.QTimer()
		self.str=self.tr("Getting title")
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.progress)
	
	def run(self):
		self.ui.linkDesc.setText(self.str)

		self.timer.start(1)
		self.timer.setInterval(400)

		sock = urllib.urlopen(self.url)
		reader=codecs.getreader('utf-8')
		try:
			sock=reader(sock)
			htmlSource = sock.read()
		except:
			sock = urllib.urlopen(self.url)
			htmlSource = sock.read()
		sock.close()
		idx1=htmlSource.find("<title>")
		idx2=htmlSource.find("</title>",idx1)
		self.timer.stop()

		self.title=htmlSource[idx1+len("<title>"):idx2].strip()
		try:
			self.unescape()
		except: pass
		self.addLink(self.url,self.title)
		
	def unescape(self):
		self.title= re.sub('&(%s);' % '|'.join(name2codepoint), 
				lambda m: unichr(name2codepoint[m.group(1)]), self.title)

	def progress(self):
		text=self.ui.linkDesc.text()
		text+="."
		self.ui.linkDesc.setText(text)
	def addLink(self,name,desc):
		a = QtGui.QTreeWidgetItem(self.ui.linkslist)
		a.setText(0, name)
		a.setText(1, desc)
		self.parent.project.links[name]=desc
		self.parent.project.Save("links")
		self.ui.linkUrl.clear()
		self.ui.linkDesc.clear()
