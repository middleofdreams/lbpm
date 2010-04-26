#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import main
from PyQt4 import QtCore,QtGui

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	locale = QtCore.QLocale.system().name()
	qtTranslator = QtCore.QTranslator()

	if qtTranslator.load("lbpm_" + locale, ":tlumaczenia/"):
		app.installTranslator(qtTranslator)
	myapp = main.LBPM()
	myapp.show()
	app.exec_()

