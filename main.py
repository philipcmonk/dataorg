#!/usr/bin/python

from Tkinter import *
import ttk
from PIL import Image, ImageTk

class Application(Frame):
	def say_hi(self):
		print "hi there, everyone!"
	
	def createWidgets(self):
		self.chooseTrial = Label(self)
		self.chooseTrial["text"] = "This is where you'll be able to\nchoose which trial to examine"
		self.chooseTrial.pack()

		self.trialLabel = Label(self)
		self.trialLabel["text"] = "F13001"
		self.trialLabel.pack()

		self.nb = ttk.Notebook(self)
		self.makeTabs(self.nb)
		for title,tab in self.tabs:
			self.nb.add(tab, text=title)
		self.nb.pack()

	def makeTabs(self,nb):
		self.tabs = []
		frame = Frame(nb)
		frame.grid()

		xrdProcessed = ttk.Notebook(frame)

		images = ["only", "all"]

		for img in images:
			image = Image.open("F13001SAL_%s.jpg" % img)
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

		xrdGraphs = Label(frame)
		xrdGraphs["text"] = ["XRD\n", "graphs"]
		xrdGraphs.grid(column = 1, row = 0)

		fesem = Label(frame)
		fesem["text"] = ["FESEM\n", "data"]
		fesem.grid(column = 2, row = 0)

		experimentNotes = Text(frame)
		experimentNotes["height"] = 5
		experimentNotes.insert("1.0", "Experiment notes will go here")
		experimentNotes.grid(column = 2, row = 1)

		self.tabs.append( ("SAL", frame) )

#		button = Button(frame)
#		button["text"] = "yo"
#		button["command"] = self.quit
#		button.grid()
#		self.tabs.append( ("SAL", frame) )

#		self.master = Label(self)
#		self.master["text"] = "F13001"
#		self.master.grid()
#
#		self.tabs = ttk.Notebook(self)
#	
#		self.QUIT = Button(self.tabs)
#		self.QUIT["text"] = "QUIT"
#		self.QUIT["fg"]   = "red"
#		self.QUIT["command"] =  self.quit
#		
#		self.QUIT.grid()
#		
#		self.hi_there = Button(self.tabs)
#		self.hi_there["text"] = "Hello",
#		self.hi_there["command"] = self.say_hi
#		
#		self.hi_there.grid()
#
#		self.tabs.add(self.hi_there, text="hi")
#		self.tabs.add(self.QUIT, text="goodbye")
#		self.tabs.grid()

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

