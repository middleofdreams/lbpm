# -*- coding: utf-8 -*-

import datetime,os
class Todays(object):
	def __init__(self,collection="default"):
		self.collection=collection
		now=datetime.datetime.now()
		self.date="%i-%i-%i" %(int(now.day),int(now.month),int(now.year))
		self.check_files()
		self.load_jobs()
		
	def check_files(self):
		workpath=os.environ['HOME']+"/.lbpm/"
		path=workpath+self.collection+"/_todays_"
		if not os.path.isdir(path):
			os.makedirs(path)
		try:
			f=open(path+"/"+self.date+".list",'r')
			jobs=f.read().split("\n")
		except:
			f=open(path+"/"+self.date+".list",'w')
			jobs=[]
		f.close()
		self.raw_jobs=jobs
	def load_jobs(self):
		self.jobs=[]
		for job in self.raw_jobs:
			line=job.split("|",1)
			job=TodaysJob(line)
			self.jobs.append(job)
			
	def check_job(self,name,project):
		ret=False
		for job in self.jobs:
			if job.name==name and job.project==project: ret=True
		return ret
			
	def save_jobs(self):
		workpath=os.environ['HOME']+"/.lbpm/"
		path=workpath+self.collection+"/_todays_"
		file=""
		for job in self.jobs:
			try:
				line=job.project+"|"+job.name
				file+=line+"\n"
			except:
				pass
		
		f=open(path+"/"+self.date+".list",'w')
		f.write(file)
		f.close()
			
class TodaysJob(object):
	name=""
	project=""
	
	def __init__(self,line):
		try: 
			self.project,self.name=line
		except:
			self.name,self.project=(None,None)
				
	
