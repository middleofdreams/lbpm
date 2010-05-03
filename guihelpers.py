# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
def message(title,text,onlyok=False):
		msgBox=QtGui.QMessageBox()
		msgBox.setWindowTitle(title)
		msgBox.setText(text)
		msgBox.setTextFormat(1)

		msgBox.addButton("OK",QtGui.QMessageBox.AcceptRole)
		if not onlyok:
			msgBox.addButton(msgBox.tr("Cancel"),QtGui.QMessageBox.RejectRole)
		ret = msgBox.exec_()
		return ret
def about():
		msgBox=QtGui.QMessageBox()
		msgBox.setWindowTitle("About")
		msgBox.setText("<B><font size=+2>LadyBug Project Manager</font><br/><center>0.2</center></b>")
		msgBox.setTextFormat(1)
		msgBox.setInformativeText(u"LBPM is an application for collecting information, text, links, jobs about every project you participate in.\n\nCopyright Kuba Wrożyna")
		msgBox.addButton("Close",QtGui.QMessageBox.AcceptRole)
		
		ret = msgBox.exec_()
		return ret

def jobStatusColor(item,current,statuses):
		if current==statuses[1]:
			for i in range(5):
				try:
					item.setBackgroundColor(i, QtGui.QColor(255, 255, 144))
				except:
					pass
		
		elif current==statuses[2]:
			for i in range(5):
				try:
					item.setBackgroundColor(i, QtGui.QColor(67, 204, 49))
				except:
					pass
		else:
			for i in range(5):
				try:
					item.setBackgroundColor(i, QtGui.QColor(255, 255, 255))
				except:
					pass
		return item
