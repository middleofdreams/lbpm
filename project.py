# -*- coding: utf-8 -*-

import os,codecs
class Project(object):
	notes={}
	documents={}
	links={}
	jobs={}
	
	def __init__(self,name):
		self.name=name
	
	def Save(self,what,collection="default"):
		workpath=os.environ['HOME']+"/.lbpm/"
		collection_path=workpath+collection
		path=collection_path+"/"+self.name+"/"+what+".list"
		if what=="notes":list=self.notes
		if what=="documents":list=self.documents
		if what=="links":list=self.links
		if what=="jobs":list=self.jobs
		file=""
		for i in list:
			if what=="jobs":
				note=list[i][2]
				if note==None: note="--"
				line=i+"|"+list[i][0]+"|"+list[i][1]+"|"+note
			else:
				content=list[i].replace("\n","<br/>")
				line=i+"|"+unicode(content)
			file+=line+"\n"
		f=codecs.open(path,'w', "utf-8")
		f.write(unicode(file))
		
