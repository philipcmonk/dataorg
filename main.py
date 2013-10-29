#!/usr/bin/python

from Tkinter import *
import ttk
from PIL import Image, ImageTk
import os
import re

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
		xrdNotes["height"] = 5
		xrdNotes.insert("1.0","XRD notes will go here")
		xrdNotes.grid(column = 0, row = 1)

		if not os.path.isfile("data/%s_graph.png" % self.fileroot) or \
		   os.path.getmtime("data/%s_graph.png" % self.fileroot) < os.path.getmtime("XRD/Processed/%s.txt" % self.fileroot) or \
		   os.path.getmtime("data/%s_graph.png" % self.fileroot) < os.path.getmtime("createplot.r"):
			os.system("Rscript createplot.r %s" % self.fileroot)

		img = Image.open("data/%s_graph.png" % self.fileroot)
		graph = ImageTk.PhotoImage(img)

		xrdGraphs = Label(frame,image=graph)
		xrdGraphs.image = graph
		xrdGraphs.grid(column = 1, row = 0)

		fesem = Label(frame)
		fesem["text"] = ["FESEM\n", "data"]
		fesem.grid(column = 2, row = 0)

		experimentNotes = Text(frame)
		experimentNotes["height"] = 5
		experimentNotes.insert("1.0", "Experiment notes will go here")
		experimentNotes.grid(column = 2, row = 1)

		self.tabs.append( (self.fileroot, frame) )

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

