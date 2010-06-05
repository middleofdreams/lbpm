# -*- coding: utf-8 -*-

import sys,os,subprocess,datetime
from PyQt4 import QtCore, QtGui
from manageprojects_ui import *

from loadproject import *
import guihelpers
from filter import *
import todays
import getHTMLTitle
from logs import Logs
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
		now=datetime.date.today()
		nt=datetime.time(0,0)
		now=datetime.datetime.combine(now,nt)+datetime.timedelta(days=1)
		
		self.ui.jobTime.setDateTime(now)


		for i in self.collection.projects:
			self.ui.projectslist.addItem(self.collection.projects[i].name)
		self.ui.tabs.setDisabled(True)
		self.ui.todaysFrame.setVisible(False)
		self.todays=todays.Todays()
		self.loadTodays()
		
		self._statuses=[self.tr('New'),self.tr("In progress"),self.tr("Done")]
		self.logs=Logs(self.ui.statusBar,self.tr("LBPM initialized"))
	@QtCore.pyqtSlot()		
	def on_jobTimeCheck_clicked(self):
		if self.ui.jobTime.isEnabled():
			self.ui.jobTime.setDisabled(True)
		else:
			self.ui.jobTime.setDisabled(False)
	def on_notetext_textChanged(self):
		self.ui.noteSave.setEnabled(True)	
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
				
	
	@QtCore.pyqtSlot()				
	def on_op1_clicked(self):self.changeOp(1)
	@QtCore.pyqtSlot()	
	def on_op2_clicked(self):self.changeOp(2)
	@QtCore.pyqtSlot()	
	def on_op3_clicked(self):self.changeOp(3)
	
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

	def on_actionAbout_activated(self):	
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
		stats=unicode(self.tr("Documents: %i\nNotes: %i\nLinks: %i\nTasks: %i")) %(0,0,0,0)
		self.ui.projectStatistics.setText(stats)	
		stats=unicode(self.tr("New: %i\nIn progress: %i\nDone: %i")) %(0,0,0)
		self.ui.projectJobsStatistics.setText(stats)
		self.ui.projectName.setText(self.tr("No project selected"))
	def on_projectslist_itemActivated(self,e):
		self.ui.tabs.setDisabled(False)
		project=unicode(e.text())
		self.clearall()
		self.ui.projectName.setText(project.capitalize())
		self.setWindowTitle(project.capitalize()+ " - LadyBug Project Manager")
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
		self.ui.noteSave.setEnabled(False)
		self.logs.add(self.tr("Project '%s' loaded" %e.text()))

	def updateStats(self):
		docs=len(self.project.documents)
		notes=len(self.project.notes)
		links=len(self.project.links)
		jobs=len(self.project.jobs)
		
		stats=unicode(self.tr("Documents: %i\nNotes: %i\nLinks: %i\nTasks: %i")) %(docs,notes,links,jobs)
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

			
	def on_noteslist_itemActivated(self,e):
		if self.ui.noteSave.isEnabled():
			ret=guihelpers.message(self.tr("Warning"),self.tr("All changes made in previous note will be lost. Proceed?"))
			if ret!=0: return 0
		note=unicode(e.text())
		text=self.project.notes[note]
		self.ui.notetext.clear()
		self.ui.notetext.append(text.replace("<br/>","\n"))
		self.note=note
		self.ui.notetext.setDisabled(False)
		self.ui.noteSave.setEnabled(False)
		self.logs.add(self.tr("Note '%s' opened" %e.text()))

	def on_docslist_itemActivated(self,e):
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
		self.logs.add(self.tr("Document '%s' selected" %e.text()))


	@QtCore.pyqtSlot()	
	def on_noteSave_clicked(self):
		text=self.ui.notetext.toPlainText()
		self.project.notes[self.note]=text
		self.project.Save("notes")
		self.ui.noteSave.setEnabled(False)
		self.logs.add(self.tr("Note '%s' saved" %self.note))

	@QtCore.pyqtSlot()		
	def on_noteCreate_clicked(self):
		name=self.ui.newnote.text()
		name=unicode(name).strip()
		if name=="" or name in self.project.notes:
			guihelpers.message(self.tr("Error"),self.tr("No name specified or already exists"),True)
	
		else:
			if self.ui.noteSave.isEnabled():
				ret=guihelpers.message(self.tr("Warning"),self.tr("All changes made in previous note will be lost. Proceed?"))
				if ret!=0: return 0
			self.ui.noteslist.addItem(name)
			self.project.notes[name]=""
			self.project.Save("notes")
			self.ui.newnote.clear()
			i=self.ui.noteslist.count()
			self.ui.noteslist.setCurrentRow(i-1)
			self.ui.notetext.clear()
			self.note=name
			self.ui.notetext.setDisabled(False)
			self.logs.add(self.tr("Note '%s' created" %name))

		self.updateStats()
		self.jobNotesUpdate()
	@QtCore.pyqtSlot()	
	def on_noteDelete_clicked(self):
		item=self.ui.noteslist.currentItem()
		n=self.ui.noteslist.currentRow()
		
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No note selected"),True)
		else:
			ret=guihelpers.message(self.tr("Warning"),self.tr("Do you really want to delete note \"")+item.text()+"\" ?")
			if ret==0:
				self.ui.noteslist.takeItem(n)
				del self.project.notes[unicode(item.text())]
				self.project.Save("notes")
				self.ui.notetext.clear()
				self.ui.notetext.setDisabled(True)
				self.updateStats()
				self.jobNotesUpdate()
				self.logs.add(self.tr("Note '%s' deleted" %item.text()))


	@QtCore.pyqtSlot()			
	def on_projectCreate_clicked(self):
		name=unicode(self.ui.newProject.text())
		name=name.strip()
		if name=="" or name in self.collection.projects:
			guihelpers.message(self.tr("Error"),self.tr("No name specified or project already exists"),True)
		else:
			self.collection.create_project(name)
			self.ui.projectslist.addItem(name)
			self.ui.newProject.clear()
			self.logs.add(self.tr("Project '%s' created" %name))
	@QtCore.pyqtSlot()			
	def on_projectDelete_clicked(self):
		item=self.ui.projectslist.currentItem()
		n=self.ui.projectslist.currentRow()

		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No project selected"),True)
		else:
			ret=guihelpers.message(self.tr("Warning"),self.tr("Do you really want to delete project \"")+item.text()+"\" ?")
			if ret==0:
				try:
					project=self.project
				except:
					project=None
				if self.collection.projects[unicode(item.text())]==project:
					self.clearall()
					self.ui.tabs.setDisabled(True)
					
				self.ui.projectslist.takeItem(n)
				self.collection.delete_project(unicode(item.text()))
				self.logs.add(self.tr("Project '%s' deleted" %item.text()))

	@QtCore.pyqtSlot()				
	def on_docCreate_clicked(self):
		fd = QtGui.QFileDialog()
		path=fd.getOpenFileName()
		file=unicode(path).split("/")
		file=file[len(file)-1]
		self.project.documents[file]=path
		self.project.Save("documents")
		self.ui.docslist.addItem(file)
		self.updateStats()
		self.logs.add(self.tr("Document '%s' added" %file))


		return 0
	@QtCore.pyqtSlot()		
	def on_docOpen_clicked(self):
		item=self.ui.docslist.currentItem()
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No document selected"),True)
		else:
			text=self.project.documents[unicode(item.text())]
			subprocess.Popen(["xdg-open",text])
			self.logs.add(self.tr("Document '%s' opened" %text))

	@QtCore.pyqtSlot()		
	def on_docDelete_clicked(self):
		item=self.ui.docslist.currentItem()
		n=self.ui.docslist.currentRow()

		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No document selected"),True)
		else:
			ret=guihelpers.message(self.tr("Warning"),self.tr("This application only removes \"")+item.text()+self.tr("\" from list. Proceed?"))
			if ret==0:			
				self.ui.docslist.takeItem(n)
				del self.project.documents[unicode(item.text())]
				self.project.Save("documents")
				self.ui.doctext.clear()
				self.updateStats()
				self.logs.add(self.tr("Document '%s' deleted" %item.text()))


	@QtCore.pyqtSlot()				
	def on_linkCreate_clicked(self):
		name=self.ui.linkUrl.text()
		name=unicode(name).strip()
		desc=self.ui.linkDesc.text()
		desc=unicode(desc).strip()
		if not name.startswith("http://"): name="http://"+name

		if name=="http://" or name in self.project.links:
			guihelpers.message(self.tr("Error"),self.tr("No link specified or already exists"),True)
	
		else:
			a = QtGui.QTreeWidgetItem(self.ui.linkslist)
			a.setText(0, name)
			a.setText(1, desc)
			self.project.links[name]=desc
			self.project.Save("links")
			self.ui.linkUrl.clear()
			self.ui.linkDesc.clear()
			self.updateStats()
			self.logs.add(self.tr("Link created"))

	@QtCore.pyqtSlot()			
	def on_linkDescGet_clicked(self):
		name=self.ui.linkUrl.text()
		name=unicode(name).strip()
		self.ui.linkDesc.setText("")
		if not name.startswith("http://"): name="http://"+name
		self.ui.linkUrl.setDisabled(True)
		self.ui.linkDesc.setDisabled(True)
		self.ui.linkDescGet.setDisabled(True)
		self.ui.linkDesc.setText(self.tr("Getting title"))
		self.loader=getHTMLTitle.TitleLoader(name)
		self.loader.start()

		QtCore.QObject.connect(self.loader,QtCore.SIGNAL("finished()"), self.linkDescGetDone)
		QtCore.QObject.connect(self.loader.timer, QtCore.SIGNAL("timeout()"), self.linkDescGetProgress)

	def linkDescGetProgress(self):
		text=self.ui.linkDesc.text()
		text+="."
		self.ui.linkDesc.setText(text)	
	
	def linkDescGetDone(self):
		self.ui.linkDesc.setText(self.loader.title)
		self.ui.linkUrl.setDisabled(False)
		self.ui.linkDesc.setDisabled(False)
		self.ui.linkDescGet.setDisabled(False)
		self.logs.add(self.tr("Link description dowloaded"))

		
		
		
	def on_linkslist_itemActivated(self,e):
		url= unicode(e.text(0))
		if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("ftp://"):
			url="http://"+url
		subprocess.Popen(["xdg-open",url])
		self.logs.add(self.tr("Link opened"))

		
	def on_jobslist_itemActivated(self,e):
		note= unicode(e.text(3))
		self.OpenPopupNote(note,self.project)
	
	def on_todaysJobsList_itemActivated(self,e):
		note= unicode(e.text(4))
		project=unicode(e.text(0))
		project=self.collection.projects[project]
		self.OpenPopupNote(note,project)
		
	def OpenPopupNote(self,note,project):
		if note!="--":
			try:
				note=project.notes[note]
				guihelpers.message(self.tr("Assigned Note"),note,True)
			except:
				guihelpers.message(self.tr("Error"),self.tr("Something goes wrong. You've apparently deleted that note"),True)
	@QtCore.pyqtSlot()	
	def on_linkDelete_clicked(self):
		item=self.ui.linkslist.currentItem()
		n=self.ui.linkslist.indexOfTopLevelItem(item)

		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No link selected"),True)
		else:
			ret=guihelpers.message(self.tr("Warning"),self.tr("Do you really want to delete link \"")+item.text(0)+"\" ?")
			if ret==0:	
				del self.project.links[unicode(item.text(0))]
				self.ui.linkslist.takeTopLevelItem(n)

				self.project.Save("links")
				self.logs.add(self.tr("Link deleted"))

		self.updateStats()
	@QtCore.pyqtSlot()		
	def on_jobCreate_clicked(self):
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
			guihelpers.message(self.tr("Error"),self.tr("No task specified or already exists"),True)
	
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
			self.logs.add(self.tr("Task '%s' created" %name))

	@QtCore.pyqtSlot()	
	def on_jobDelete_clicked(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No task selected"),True)
		else:
			ret=guihelpers.message(self.tr("Warning"),self.tr("Do you really want to delete task \"")+item.text(0)+"\" ?")
			if ret==0:	
				del self.project.jobs[unicode(item.text(0))]
				self.ui.jobslist.takeTopLevelItem(n)

				self.project.Save("jobs")
				self.updateStats()
				self.updateJobsStats()
				self.logs.add(self.tr("Task '%s' deleted" %item.text(0)))


	@QtCore.pyqtSlot()				
	def on_jobEdit_clicked(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No task selected"),True)
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
			self.logs.add(self.tr("Task '%s' edited" %item.text(0)))

	@QtCore.pyqtSlot()	
	def on_jobAssignNote_clicked(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No task selected"),True)
		else:
			note=unicode(self.ui.jobNotes.currentText())
			if note==self.tr("None"): note="--"
			item=self.ui.jobslist.takeTopLevelItem(n)
			
			self.project.jobs[unicode(item.text(0))][2]=note
			item.setText(3,note)
			
			self.ui.jobslist.insertTopLevelItem(n,item)
			self.ui.jobslist.setCurrentItem(item)

			self.project.Save("jobs")
			self.loadTodays()
			self.logs.add(self.tr("Note '%s' assigned to task '%s'" %(note,item.text(0))))

	@QtCore.pyqtSlot()			
	def on_jobAddToTodays_clicked(self):
		item=self.ui.jobslist.currentItem()
		n=self.ui.jobslist.indexOfTopLevelItem(item)
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No task selected"),True)
		else:
			name=unicode(item.text(0))
			if self.todays.check_job(name,self.project.name):
				guihelpers.message(self.tr("Error"),self.tr("Task already on the list"),True)
			else:
				p=todays.TodaysJob([self.project.name,name])
				self.todays.jobs.append(p)
				self.todays.save_jobs()
				self.loadTodays()
				self.logs.add(self.tr("Task '%s' added to Todays list" %item.text(0)))

	@QtCore.pyqtSlot()				
	def on_todaysDelete_clicked(self):
		item=self.ui.todaysJobsList.currentItem()
		n=self.ui.todaysJobsList.indexOfTopLevelItem(item)
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No task selected"),True)
		else:
			project=unicode(item.text(0))
			name=unicode(item.text(1))

			for job in self.todays.jobs:
				if job.name==name and job.project==project:
					self.todays.jobs.pop(self.todays.jobs.index(job))
			self.todays.save_jobs()
			self.loadTodays()
			self.logs.add(self.tr("Task '%s' deleted from todays list" %item.text(0)))

	
	@QtCore.pyqtSlot()	
	def on_todaysNew_clicked(self):
		self.todaysJobEdit(self._statuses[0])
	@QtCore.pyqtSlot()	
	def on_todaysDone_clicked(self):
		self.todaysJobEdit(self._statuses[1])
	@QtCore.pyqtSlot()	
	def on_todaysInprogress_clicked(self):
		self.todaysJobEdit(self._statuses[2])	
				
	def todaysJobEdit(self,status):
		item=self.ui.todaysJobsList.currentItem()
		n=self.ui.todaysJobsList.indexOfTopLevelItem(item)
		
		if item==None:
			guihelpers.message(self.tr("Error"),self.tr("No task selected"),True)
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
			self.logs.add(self.tr("Task '%s' edited" %item.text(0)))

