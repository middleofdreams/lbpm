# -*- coding: utf-8 -*-

import sys,os,subprocess
from PyQt4 import QtCore, QtGui
from manageprojects_ui import *

from loadproject import *
import guihelpers
from filter import *
import todays
from getHTMLTitle import *

class LBPM(QtGui.QMainWindow):
	setcollection="default"

	def __init__(self, parent=None):
		
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_ManageProjects()
		self.ui.setupUi(self)
		self.collection=LoadProjects()
		self.ui.projectslist.clear()
		self.ui.jobslist.setColumnWidth(0,200)

		self.ui.jobslist.setColumnWidth(1,130)
		self.ui.jobslist.setColumnWidth(2,120)
		self.ui.linkslist.setColumnWidth(0,200)

		
		
		QtCore.QObject.connect(self.ui.projectslist,QtCore.SIGNAL("itemActivated(QListWidgetItem *)"), self.load_project)
		QtCore.QObject.connect(self.ui.noteslist,QtCore.SIGNAL("itemActivated(QListWidgetItem *)"), self.load_note)
		QtCore.QObject.connect(self.ui.docslist,QtCore.SIGNAL("itemActivated(QListWidgetItem *)"), self.load_doc)
		QtCore.QObject.connect(self.ui.noteSave,QtCore.SIGNAL("clicked()"), self.noteSave)
		QtCore.QObject.connect(self.ui.noteCreate,QtCore.SIGNAL("clicked()"), self.noteCreate)
		QtCore.QObject.connect(self.ui.noteDelete,QtCore.SIGNAL("clicked()"), self.noteDelete)
		QtCore.QObject.connect(self.ui.projectCreate,QtCore.SIGNAL("clicked()"), self.projectCreate)
		QtCore.QObject.connect(self.ui.projectDelete,QtCore.SIGNAL("clicked()"), self.projectDelete)
		QtCore.QObject.connect(self.ui.docCreate,QtCore.SIGNAL("clicked()"), self.docCreate)
		QtCore.QObject.connect(self.ui.docOpen,QtCore.SIGNAL("clicked()"), self.docOpen)
		QtCore.QObject.connect(self.ui.docDelete,QtCore.SIGNAL("clicked()"), self.docDelete)
		QtCore.QObject.connect(self.ui.linkCreate,QtCore.SIGNAL("clicked()"), self.linkCreate)
		QtCore.QObject.connect(self.ui.linkslist,QtCore.SIGNAL("itemActivated(QTreeWidgetItem *,int)"), self.linkOpen)
		QtCore.QObject.connect(self.ui.linkDelete,QtCore.SIGNAL("clicked()"), self.linkDelete)
		QtCore.QObject.connect(self.ui.jobCreate,QtCore.SIGNAL("clicked()"), self.jobCreate)
		QtCore.QObject.connect(self.ui.jobEdit,QtCore.SIGNAL("clicked()"), self.jobEdit)
		QtCore.QObject.connect(self.ui.jobDelete,QtCore.SIGNAL("clicked()"), self.jobDelete)
		QtCore.QObject.connect(self.ui.actionAbout,QtCore.SIGNAL("activated()"), self.aabout)
		QtCore.QObject.connect(self.ui.op1,QtCore.SIGNAL("clicked()"), self.changeOp1)
		QtCore.QObject.connect(self.ui.op2,QtCore.SIGNAL("clicked()"), self.changeOp2)
		QtCore.QObject.connect(self.ui.op3,QtCore.SIGNAL("clicked()"), self.changeOp3)
		QtCore.QObject.connect(self.ui.jobAssignNote,QtCore.SIGNAL("clicked()"), self.jobAssignNote)
		QtCore.QObject.connect(self.ui.jobslist,QtCore.SIGNAL("itemActivated(QTreeWidgetItem *,int)"), self.jobOpenNote)
		QtCore.QObject.connect(self.ui.jobAddToTodays,QtCore.SIGNAL("clicked()"), self.jobAddToTodays)
		QtCore.QObject.connect(self.ui.todaysDelete,QtCore.SIGNAL("clicked()"), self.todaysDelete)
		QtCore.QObject.connect(self.ui.todaysNew,QtCore.SIGNAL("clicked()"), self.todaysJobNew)
		QtCore.QObject.connect(self.ui.todaysDone,QtCore.SIGNAL("clicked()"), self.todaysJobDone)
		QtCore.QObject.connect(self.ui.todaysInprogress,QtCore.SIGNAL("clicked()"), self.todaysJobInprogress)
		QtCore.QObject.connect(self.ui.todaysJobsList,QtCore.SIGNAL("itemActivated(QTreeWidgetItem *,int)"), self.todaysOpenNote)
		QtCore.QObject.connect(self.ui.jobTimeCheck,QtCore.SIGNAL("clicked()"), self.jobTimeCheck)

		for i in self.collection.projects:
			self.ui.projectslist.addItem(self.collection.projects[i].name)
		self.ui.tabs.setDisabled(True)
		self.ui.todaysFrame.setVisible(False)
		self.todays=todays.Todays()
		self.loadTodays()
		
		self._statuses=[self.tr('New'),self.tr("In progress"),self.tr("Done")]
		
	def jobTimeCheck(self):
		if self.ui.jobTime.isEnabled():
			self.ui.jobTime.setDisabled(True)
		else:
			self.ui.jobTime.setDisabled(False)
		
	def loadTodays(self):
		self.ui.todaysJobsList.clear()
		for job in self.todays.jobs:
			project=job.project
			name=job.name
			try:
				status=self.collection.projects[project].jobs[name][1]
				notes=self.collection.projects[project].jobs[name][2]
				deadline=self.collection.projects[project].jobs[name][0]

				a = QtGui.QTreeWidgetItem(self.ui.todaysJobsList)
				a.setText(0,project)
				a.setText(1,name)
				a.setText(2,status)
				a.setText(3,deadline)
				a.setText(4,notes)

				a=guihelpers.jobStatusColor(a,status,self._statuses)
			except: 
				deadline=None
				status=None
				
	
				
	def changeOp1(self):self.changeOp(1)
	def changeOp2(self):self.changeOp(2)
	def changeOp3(self):self.changeOp(3)
	
	def changeOp(self,op):
		
		if op==1: w=self.ui.projectsFrame
		if op==2: w=self.ui.tabs
		if op==3: w=self.ui.todaysFrame
		
		if w.isVisible():  
			w.setVisible(False)
			if op==3: 
				self.ui.op2.setEnabled(False)
				self.ui.op2.setChecked(True)
				self.ui.tabs.setVisible(True)
		else: 
			w.setVisible(True)
			if op==3:
				self.ui.op2.setEnabled(True)

	def aabout(self):	
		guihelpers.about()
		
	def jobNotesUpdate(self):
		self.ui.jobNotes.clear()
		self.ui.jobNotes.addItem(self.tr("None"))

		for i in self.project.notes:
			self.ui.jobNotes.addItem(i)
	def clearall(self):
		self.ui.noteslist.clear()
		self.ui.docslist.clear()
		self.ui.jobslist.clear()
		self.ui.linkslist.clear()
		self.ui.notetext.clear()
		self.ui.doctext.clear()
		self.ui.notetext.setDisabled(True)
		self.ui.doctext.setDisabled(True)
		
	def load_project(self,e):
		self.ui.tabs.setDisabled(False)
		project=unicode(e.text())
		self.clearall()
		self.ui.projectName.setText(project.capitalize())
		project=self.collection.projects[project]

		for i in project.notes:
			self.ui.noteslist.addItem(i)
		for i in project.documents:
			self.ui.docslist.addItem(i)
		for i in project.links:
			a = QtGui.QTreeWidgetItem(self.ui.linkslist)
			a.setText(0, i)
			a.setText(1, project.links[i])
		self.loadJobs(project)
		self.project=project
		self.updateStats()
		self.updateJobsStats()
		self.jobNotesUpdate()
	def updateStats(self):
		docs=len(self.project.documents)
		notes=len(self.project.notes)
		links=len(self.project.links)
		jobs=len(self.project.jobs)
		
		stats=unicode(self.tr("Documents: %i\nNotes: %i\nLinks: %i\nJobs: %i")) %(docs,notes,links,jobs)
		self.ui.projectStatistics.setText(stats)		
			
	def updateJobsStats(self):
		new=0
		in_progress=0
		done=0
		
		for i in self.project.jobs:
			status=self.project.jobs[i][1]
			if status==self._statuses[0]:new+=1
			elif status==self._statuses[0]:done+=1
			else: in_progress+=1
		stats=unicode(self.tr("New: %i\nIn progress: %i\nDone: %i")) %(new,in_progress,done)
		self.ui.projectJobsStatistics.setText(stats)		

	def loadJobs(self,project):
		self.ui.jobslist.clear()
		for i in project.jobs:
			a = QtGui.QTreeWidgetItem(self.ui.jobslist)
			note=project.jobs[i][2]
			if note==None: note="--"
			a.setText(0, i)
			a.setText(1, project.jobs[i][0])
			a.setText(2, project.jobs[i][1])
			a.setText(3, note)

			status=project.jobs[i][1]
			a=guihelpers.jobStatusColor(a,status,self._statuses)

			
	def load_note(self,e):
		note=unicode(e.text())
		text=self.project.notes[note]
		self.ui.notetext.clear()
		self.ui.notetext.append(text.replace("<br/>","\n"))
		self.note=note
		self.ui.notetext.setDisabled(False)
	def load_doc(self,e):
		doc=unicode(e.text())
		text=self.project.documents[doc]
		self.ui.doctext.clear()
		if docpreview(unicode(text)):
			f=open(text,'r')
			text=f.read()
			f.close()
		else:
			text=self.tr("Sorry\nPreview not avalaible")
		self.ui.doctext.append(text)
		self.ui.doctext.setDisabled(False)


	def noteSave(self):
		text=self.ui.notetext.toPlainText()
		self.project.notes[self.note]=text
		self.project.Save("notes")
		
	def noteCreate(self):
		name=self.ui.newnote.text()
		name=unicode(name).strip()
		if name=="" or name in self.project.notes:
			guihelpers.message(self.tr("Error"),self.tr("No name specified or already exists"),True)
	
		else:
			self.ui.noteslist.addItem(name)
			self.project.notes[name]=""
			self.project.Save("notes")
			self.ui.newnote.clear()
			i=self.ui.noteslist.count()
			self.ui.noteslist.setCurrentRow(i-1)
			self.ui.notetext.clear()
			self.note=name
			self.ui.notetext.setDisabled(False)
		self.updateStats()
		self.jobNotesUpdate()

	def noteDelete(self):
		item=self.ui.noteslist.currentItem()
		n=self.ui.noteslist.currentRow()
		
		if item==None:
			guihelpers.message("Error","No note selected",True)
		else:
			ret=guihelpers.message("Warning","Do you really want to delete note \""+item.text()+"\" ?")
			if ret==0:
				self.ui.noteslist.takeItem(n)
				del self.project.notes[unicode(item.text())]
				self.project.Save("notes")
				self.ui.notetext.clear()
				self.ui.notetext.setDisabled(True)
				self.updateStats()
				self.jobNotesUpdate()

				
	def projectCreate(self):
		name=unicode(self.ui.newProject.text())
		name=name.strip()
		if name=="" or name in self.collection.projects:
			guihelpers.message("Error","No name specified or project already exists",True)
		else:
			self.collection.create_project(name)
			self.ui.projectslist.addItem(name)
			self.ui.newProject.clear()
			
	def projectDelete(self):
		item=self.ui.projectslist.currentItem()
		n=self.ui.projectslist.currentRow()

		if item==None:
			guihelpers.message("Error","No project selected",True)
		else:
			ret=guihelpers.message("Warning","Do you really want to delete project \""+item.text()+"\" ?")
			if ret==0:
				try:
					project=self.project
				except:
					project=None
				if self.collection.projects[unicode(item.text())]==project:
					self.clearall()
					self.ui.tabWidget.setDisabled(True)
					
				self.ui.projectslist.takeItem(n)
				self.collection.delete_project(unicode(item.text()))
				
				
	def docCreate(self):
		fd = QtGui.QFileDialog()
		path=fd.getOpenFileName()
		file=unicode(path).split("/")
		file=file[len(file)-1]
		self.project.documents[file]=path
		self.project.Save("documents")
		self.ui.docslist.addItem(file)
		self.updateStats()

		return 0
		
	def docOpen(self):
		item=self.ui.docslist.currentItem()
		if item==None:
			guihelpers.message("Error","No document selected",True)
		else:
			text=self.project.documents[unicode(item.text())]
			subprocess.Popen(["xdg-open",text])
		
	def docDelete(self):
		item=self.ui.docslist.currentItem()
		n=self.ui.docslist.currentRow()

		if item==None:
			guihelpers.message("Error","No document selected",True)
		else:
			ret=guihelpers.message("Warning","This application only removes \""+item.text()+"\" from list. Proceed?")
			if ret==0:			
				self.ui.docslist.takeItem(n)
				del self.project.documents[unicode(item.text())]
				self.project.Save("documents")
				self.ui.doctext.clear()
				self.updateStats()

				
	def linkCreate(self):
		name=self.ui.linkUrl.text()
		name=unicode(name).strip()
		desc=self.ui.linkDesc.text()
		desc=unicode(desc).strip()
		if not name.startswith("http://"): name="http://"+name

		if name=="" or name in self.project.links:
			guihelpers.message("Error","No name specified or already exists",True)
	
		else:
			loader=TitleLoader(self,name)

			if desc=="":
				loader.start()
			else:
				loader.addLink(name,desc)
		self.updateStats()

	def linkOpen(self,e):
		url= unicode(e.text(0))
		if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("ftp://"):
			url="http://"+url
		subprocess.Popen(["xdg-open",url])
	def jobOpenNote(self,e):
		note= unicode(e.text(3))
		self.OpenPopupNote(note,self.project)
	
	def todaysOpenNote(self,e):
		note= unicode(e.text(4))
		project=unicode(e.text(0))
		project=self.collection.projects[project]
		self.OpenPopupNote(note,project)
		
	def OpenPopupNote(self,note,project):
		if note!="--":
			try:
				note=project.notes[note]
				guihelpers.message("Assigned Note",note,True)
			except:
				guihelpers.message("Error","Something goes wrong. You've apparently deleted that note",True)
	def linkDelete(self):
		item=self.ui.linkslist.currentItem()
		n=self.ui.linkslist.indexOfTopLevelItem(item)

		if item==None:
			guihelpers.message("Error","No link selected",True)
		else:
			ret=guihelpers.message("Warning","Do you really want to delete link \""+item.text(0)+"\" ?")
			if ret==0:	
				del self.project.links[unicode(item.text(0))]
				self.ui.linkslist.takeTopLevelItem(n)

				self.project.Save("links")
		self.updateStats()
		
	def jobCreate(self):
		name=self.ui.jobName.text()
		name=unicode(name).strip()
		if self.ui.jobTimeCheck.isChecked():
			date=self.ui.jobTime.dateTime()
			date=date.toString("dd.MM.yyyy hh:mm")
			date=unicode(date)
		else:
			date="--"
		status=self.ui.jobStatus.currentText()
		status=unicode(status)
		content=[date,status,None]
		if name=="" or name in self.project.jobs:
			guihelpers.message("Error","No job specified or already exists",True)
	
		else:
			a = QtGui.QTreeWidgetItem(self.ui.jobslist)
			a.setText(0, name)
			a.setText(1, date)
			a.setText(2, status)
			a.setText(3, "--")

			a=guihelpers.jobStatusColor(a,status,self._statuses)
			self.project.jobs[name]=content
			self.project.Save("jobs")
			self.ui.jobName.clear()
			self.updateStats()
			self.updateJobsStats()

	def jobDelete(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message("Error","No job selected",True)
		else:
			ret=guihelpers.message("Warning","Do you really want to delete job \""+item.text(0)+"\" ?")
			if ret==0:	
				del self.project.jobs[unicode(item.text(0))]
				self.ui.jobslist.takeTopLevelItem(n)

				self.project.Save("jobs")
				self.updateStats()
				self.updateJobsStats()


				
	def jobEdit(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message("Error","No job selected",True)
		else:
			item=self.ui.jobslist.takeTopLevelItem(n)
			status=self.ui.jobEditStatus.currentText()
			status=unicode(status)
			self.project.jobs[unicode(item.text(0))][1]=status
			item.setText(2,status)
			item=guihelpers.jobStatusColor(item,status,self._statuses)
	
			self.ui.jobslist.insertTopLevelItem(n,item)
			self.ui.jobslist.setCurrentItem(None)

			self.project.Save("jobs")
			self.updateJobsStats()
			self.loadTodays()

	def jobAssignNote(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message("Error","No job selected",True)
		else:
			note=unicode(self.ui.jobNotes.currentText())
			if note=="None": note="--"
			item=self.ui.jobslist.takeTopLevelItem(n)
			
			self.project.jobs[unicode(item.text(0))][2]=note
			item.setText(3,note)
			
			self.ui.jobslist.insertTopLevelItem(n,item)
			self.ui.jobslist.setCurrentItem(item)

			self.project.Save("jobs")
			self.loadTodays()
	def jobAddToTodays(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		if item==None:
			guihelpers.message("Error","No job selected",True)
		else:
			name=unicode(item.text(0))
			if self.todays.check_job(name,self.project.name):
				guihelpers.message("Error","Job already on the list",True)
			else:
				p=todays.TodaysJob([self.project.name,name])
				self.todays.jobs.append(p)
				self.todays.save_jobs()
				self.loadTodays()
				
	def todaysDelete(self):
		item=self.ui.todaysJobsList.currentItem()
		n=self.ui.todaysJobsList.indexOfTopLevelItem(item)
		if item==None:
			guihelpers.message("Error","No job selected",True)
		else:
			project=unicode(item.text(0))
			name=unicode(item.text(1))

			for job in self.todays.jobs:
				if job.name==name and job.project==project:
					self.todays.jobs.pop(self.todays.jobs.index(job))
			self.todays.save_jobs()
			self.loadTodays()
	
	
	def todaysJobNew(self):
		self.todaysJobEdit(self._statuses[0])
	def todaysJobDone(self):
		self.todaysJobEdit(self._statuses[1])
	def todaysJobInprogress(self):
		self.todaysJobEdit(self._statuses[2])	
				
	def todaysJobEdit(self,status):
		item=self.ui.todaysJobsList.currentItem()
		n=self.ui.todaysJobsList.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message("Error","No job selected",True)
		else:
			item=self.ui.todaysJobsList.takeTopLevelItem(n)
			status=unicode(status)
			project=self.collection.projects[unicode(item.text(0))]
			project.jobs[unicode(item.text(1))][1]=status
			item.setText(2,status)
			item=guihelpers.jobStatusColor(item,status,self._statuses)
	
			self.ui.todaysJobsList.insertTopLevelItem(n,item)

			project.Save("jobs")
			try:
				self.updateJobsStats()
				self.loadJobs(self.project)
			except:
				pass
			self.loadTodays()
