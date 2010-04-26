# -*- coding: utf-8 -*-

import os,codecs
from project import *
class LoadProjects(object):
	
	def __init__(self,collection="default"):
		self.collection=collection
		projects,self.path=self.check_files()
		self.projects={}
		for i in projects:
			if i!="":
				pr=Project(i)
				pr.notes=self.getList("notes",i)
				pr.documents=self.getList("documents",i)
				pr.jobs=self.getList("jobs",i)
				pr.links=self.getList("links",i)
				self.projects[i]=pr
	
		
		
	def getList(self,what,i):
		list={}
		try:
			f=codecs.open(self.path+"/"+i+"/"+what+".list",'r', 'utf-8')
			lines=unicode(f.read()).split("\n")
			for i in lines:
				if what=="jobs":
					line=i.split("|",3)
					try:
						note=line[3]
					except:
						note=None
					list[line[0]]=[line[1],line[2],note]
				else:
					line=i.split("|",1)
					list[line[0]]=line[1]
		except:
			pass
		return list
		
	def check_files(self):
		workpath=os.environ['HOME']+"/.lbpm/"
		collection_path=workpath+self.collection
		if not os.path.isdir(workpath):
			os.makedirs(workpath)
		if not os.path.isdir(collection_path):
			os.makedirs(collection_path)
		try:
			f=open(collection_path+"/projects.list",'r')
			projects=f.read().split("\n")
		except:
			f=open(collection_path+"/projects.list",'w')
			projects=[]
		f.close()
		return projects,collection_path
		
	def create_project(self,name):
		workpath=os.environ['HOME']+"/.lbpm/"
		path=workpath+self.collection+"/"+name
		if os.path.isdir(path):
			import guihelpers
			guihelpers.message("Warning","Project directory already exists - using it.",True)
		else:
			os.makedirs(path)
			
		pr=Project(name)
		pr.notes=self.getList("notes",name)
		pr.documents=self.getList("documents",name)
		pr.jobs=self.getList("jobs",name)
		pr.links=self.getList("links",name)
		self.projects[name]=pr
		self.save_project_list()
		
	def save_project_list(self):
		file=""
		for i in self.projects:
			file+=i+"\n"
		workpath=os.environ['HOME']+"/.lbpm/"
		path=workpath+self.collection
		f=open(path+"/projects.list",'w')
		f.write(file)
		f.close()
		
	def delete_project(self,name):
		del self.projects[name]
		self.save_project_list()


