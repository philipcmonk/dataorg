#!/usr/bin/python

from Tkinter import *
import ttk
from PIL import Image, ImageTk
import os
import re
import csv

def selectExp(event):
	app.selectExp(event)

def closeTab(event):
	app.closeTabMiddleClick(event)

class Application(Frame):
	def scrapeExperiments(self):
		listall = os.listdir("XRD/Processed")
		self.files = [re.match(r'(...)(...)([^.]*)\.(...)',f) for f in listall]
		for m in self.files:
			if not m:
				print "File not recognized"
		self.files = [m for m in self.files if m]
		self.semesters = sorted(list(set([m.group(1) for m in self.files])),lambda x,y: (cmp(int(x[1:]),int(y[1:])) if not x[1:] == y[1:] else cmp(y[0],x[0])))
		self.numbers = []
		self.exps = []
		for sem in self.semesters:
			self.numbers.append(sorted(list(set([m.group(2) for m in self.files if m.group(1) == sem])),lambda x,y: cmp(int(x),int(y))))
			self.exps.append([])
			for n in self.numbers[-1]:
				self.exps[-1].append(sorted(list(set([m.group(3) for m in self.files if m.group(1) == sem and m.group(2) == n and m.group(4) == 'txt']))))

	def createWidgets(self):
		self.chooseTrial = ttk.Treeview(self)
		self.fillExperiments(self.chooseTrial)
		self.chooseTrial.bind('<Double-Button-1>',selectExp)
		self.chooseTrial["height"] = 35
		self.chooseTrial.pack(side=LEFT)

#		self.trialLabel = Label(self)
#		self.trialLabel["text"] = "F13001"
#		self.trialLabel.pack()

		self.nb = ttk.Notebook(self)
		self.makeTabs(self.nb)
		for title,tab in self.tabs:
			self.nb.add(tab, text=title)
		self.nb.bind("<Button-2>",closeTab)
		self.nb.enable_traversal()
		self.nb.pack()

		self.closeTabButton = Button(self)
		self.closeTabButton["text"] = "Close Tab"
		self.closeTabButton["command"] = self.closeTab
		self.closeTabButton.pack()

		self.quitButton = Button(self)
		self.quitButton["text"] = "Quit"
		self.quitButton["command"] = self.quit
		self.quitButton.pack()

	def closeTab(self):
		self.nb.forget("current")

	def closeTabMiddleClick(self,event):
		self.nb.forget("@%d,%d" % (event.x,event.y))
	
	def dispExp(self):
#		self.trialLabel["text"] = self.fileroot

		self.makeTabs(self.nb)
		for title,tab in self.tabs:
			self.nb.add(tab, text=title)


	def fillExperiments(self,tree):
		root = tree.insert('','end',text='Experiments',open=True)
		for sem,num,exp in zip(self.semesters,self.numbers,self.exps):
			sid = tree.insert(root,'end',text=sem,open=True)
			for n,ex in zip(num,exp):
				nid = tree.insert(sid,'end',text=n,open=True)
				for e in ex:
					tree.insert(nid,'end',text=e,open=True)

	def selectExp(self,event):
		tree = event.widget
		node = tree.focus()
		if tree.parent(node):
			if tree.parent(tree.parent(node)):
				if tree.parent(tree.parent(tree.parent(node))):
					for file in self.hijitosOf(tree.item(tree.parent(tree.parent(node)))["text"], tree.item(tree.parent(node))["text"], tree.item(node)["text"]):
						self.fileroot = file
						self.dispExp()
				else:
					for file in self.hijitosOf(tree.item(tree.parent(node))["text"],tree.item(node)["text"]):
						self.fileroot = file
						self.dispExp()
			else:
				for file in self.hijitosOf(tree.item(node)["text"]):
					self.fileroot = file
					self.dispExp()
		else:
			for file in self.hijitosOf():
				self.fileroot = file
				self.dispExp()

	def hijitosOf(self, semester='', number='', experiment=''):
		res = []
		for sem,num,exp in zip(self.semesters,self.numbers,self.exps):
			if semester == '' or semester == sem:
				for nu,ex in zip(num,exp):
					if number == '' or number == nu:
						for e in ex:
							if experiment == '' or experiment == e:
								res.append(sem + nu + e)
		return res

	def onModifiedXrd(self,widget,event):
		widget["text"] = "Save*"

	def saveXrdNotes(self,notes,save,fileroot):
		notes.edit_modified(0)
		f = open("data/"+fileroot+"_xrdnotes.txt",'w')
		f.write(notes.get("0.0", "end"))
		f.close()
		save["text"] = "Save"

	def saveEdNotes(self,eN,rows,eS,fileroot,appendage):
		with open("data/"+fileroot+"_exp"+appendage+".csv",'w') as csvfile:
			csvwriter = csv.writer(csvfile,delimiter='\t',quotechar='|')
			for r in rows:
				csvwriter.writerow([e.get() for e in r])

	def makeTabs(self,nb):
		self.tabs = []
		frame = Frame(nb)
		frame.grid()

		xrdProcessed = ttk.Notebook(frame)

		images = ["only", "all"]

		for img in images:
			image = Image.open("XRD/Processed/%s_%s.jpg" % (self.fileroot,img))
			image = image.resize((653,500), Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(image)
			t = Frame(xrdProcessed)
			pic = Label(t,image=photo)
			pic["height"] = 500
			pic.image = photo
			pic.grid()
			xrdProcessed.add(t,text=img)

		xrdProcessed.grid(column = 0, row = 0)

		xrdNotes = Text(frame)
		xrdSave = Button(frame)

		xrdNotes["height"] = 5
		xrdNotes.bind("<<Modified>>",lambda e:self.onModifiedXrd(xrdSave,e))
		xrdNotes.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveXrdNotes(xrdNotes,xrdSave,f))

		if os.path.isfile("data/%s_xrdnotes.txt" % self.fileroot):
			f = open("data/%s_xrdnotes.txt" % self.fileroot,'r')
			xrdNotes.insert("end",f.read())
			f.close()

		xrdNotes.edit_modified(0)

		xrdNotes.grid(column = 0, row = 1)

		xrdSave["text"] = "Save"
		xrdSave["command"] = lambda f=self.fileroot:self.saveXrdNotes(xrdNotes,xrdSave,f)
		xrdSave.grid(column = 0, row = 2)

		if not os.path.isfile("data/%s_graph.png" % self.fileroot) or \
		   os.path.getmtime("data/%s_graph.png" % self.fileroot) < os.path.getmtime("XRD/Processed/%s.txt" % self.fileroot) or \
		   os.path.getmtime("data/%s_graph.png" % self.fileroot) < os.path.getmtime("createplot.r"):
			if os.name == "nt":
				os.system(".\\runr.bat %s" % self.fileroot)
			else:
				os.system("Rscript createplot.r %s" % self.fileroot)

		img = Image.open("data/%s_graph.png" % self.fileroot)
		graph = ImageTk.PhotoImage(img)

		xrdGraphs = Label(frame,image=graph)
		xrdGraphs.image = graph
		xrdGraphs.grid(column = 1, row = 0)

		experimentNotes = Frame(frame)
		experimentSave = Button(frame)

		rows = self.fillExperimentNotes(experimentNotes,experimentSave)

		experimentNotes.grid(column = 1, row = 1)

		experimentSave["text"] = "Save"
		experimentSave["command"] = lambda f=self.fileroot:self.saveEdNotes(experimentNotes,experimentSave,rows,f)
#		experimentNotes.grid(column = 1, row = 2)

		fesem = Label(frame)
		fesem["text"] = ["FESEM\n", "data"]
		fesem.grid(column = 2, row = 0)

		self.tabs.append( (self.fileroot, frame) )

	def fillExperimentNotes(self,eN,eS):
		eN1 = Frame(eN)
		eN2 = Frame(eN)
		eN1.pack()
		eN2.pack()

		if not os.path.isfile("data/%s_exp1.csv" % self.fileroot):
			f = open("data/%s_exp1.csv" % self.fileroot,'w')
			f.write("1\ttesting\n2\tand stuff\n3\ttesting\n4\tand stuff\n5\ttesting\n6\tand stuff\n7\ttesting\n8\tand stuff")
			f.close()
		with open("data/%s_exp1.csv" % self.fileroot) as csvfile:
			exp1 = csv.reader(csvfile, delimiter="\t", quotechar = "|")
			rows1 = []
			for i,r in enumerate(exp1):
				rows1.append((Entry(eN1),Entry(eN1)))
				a,b = rows1[-1]
				a.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN1,rows1,eS,f,"1"))
				b.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN1,rows1,eS,f,"1"))
				a["width"] = 5
				a["justify"] = "right"
				a.insert("end",r[0])
				b.insert("end",r[1])
				a.grid(column = 0, row = i)
				b.grid(column = 1, row = i)

		if not os.path.isfile("data/%s_exp2.csv" % self.fileroot):
			f = open("data/%s_exp2.csv" % self.fileroot,'w')
			f.write("Act.\t12:00 AM\t01/01/2013\t1:00 AM\t01/01/2013\nCool\t1:00 AM\t01/01/2013\t2:00 AM\t01/01/2013")
			f.close()
		with open("data/%s_exp2.csv" % self.fileroot) as csvfile:
			exp2 = csv.reader(csvfile, delimiter="\t", quotechar = "|")
			rows2 = []
			for i,r in enumerate(exp2):
				rows2.append((Entry(eN2),Entry(eN2),Entry(eN2),Entry(eN2),Entry(eN2)))
				a,b,c,d,e = rows2[-1]
				a.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN2,rows2,eS,f,"2"))
				b.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN2,rows2,eS,f,"2"))
				c.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN2,rows2,eS,f,"2"))
				d.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN2,rows2,eS,f,"2"))
				e.bind("<FocusOut>",lambda e,f=self.fileroot:self.saveEdNotes(eN2,rows2,eS,f,"2"))
				a["width"] = 5
				a["justify"] = "right"
				a.insert("end",r[0])
				b.insert("end",r[1])
				c.insert("end",r[2])
				d.insert("end",r[3])
				e.insert("end",r[4])
				a.grid(column = 0, row = i)
				b.grid(column = 1, row = i)
				c.grid(column = 2, row = i)
				d.grid(column = 3, row = i)
				e.grid(column = 4, row = i)

#		row = []
#		for i in range(0,9):
#			row.append((Entry(eN),Entry(eN)))
#			a,b = row[-1]
#			a["width"] = 5
#			a["justify"] = "right"
#			a.insert("end",str(i+1))
#			a.grid(column = 2, row = i)
#			b.grid(column = 3, row = i,columnspan=2)

		

#		start = Entry(eN)
#		end = Entry(eN)
#		act = Entry(eN)
#		cool = Entry(eN)
#
#		start["width"] = 6
#		end["width"] = 6
#		act["width"] = 6
#		cool["width"] = 6
#
#		start.grid(column=1,row=8,columnspan=2)
#		end.grid(column=3,row=8,columnspan=2)
#		act.grid(column=0,row=9)
#		cool.grid(column=0,row=10)
#
#		ast = Entry(eN)
#		ast["width"] = 10
#		ast.grid(column=1,row=9)
#		asd = Entry(eN)
#		asd["width"] = 10
#		asd.grid(column=2,row=9)
#		aet = Entry(eN)
#		aet["width"] = 10
#		aet.grid(column=3,row=9)
#		aed = Entry(eN)
#		aed["width"] = 10
#		aed.grid(column=4,row=9)
#		cst = Entry(eN)
#		cst["width"] = 10
#		cst.grid(column=1,row=10)

	def __init__(self, master=None):
		self.scrapeExperiments()
		self.fileroot = "F13001SAL"
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

