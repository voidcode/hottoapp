#!/usr/bin/pyhton
from gi.repository import Gtk
import json, os
from pprint import pprint

from gi.repository import WebKit
with open("courses/php101.json") as coursefile:
	course = json.load(coursefile)

pprint("Title: "+course["name"].split(".")[-1])
pprint("File: "+course["file"])


# exams->test0->quition1->choice
pprint(course["exams"][0][1]["choice"])

pprint(course["exams"][0][1]["answer"])

#Class-------------------------------------------------STARTs
#this class load all course file into class vars
class CourseFolder:	
	global mdfiles
	global jsonfiles
	def __init__(self, coursepath):
		self.mdfiles = []
		self.jsonfiles = []
		for name in os.listdir(coursepath):
			if name.split(".")[-1] == "md" and os.path.isfile(os.path.join(coursepath, name)):
				self.mdfiles.append(name)
			elif name.split(".")[-1] == "json" and os.path.isfile(os.path.join(coursepath, name)):
				self.jsonfiles.append(name)
	def getMdFiles(self):
		return self.mdfiles
	def getJsonFiles(self):
		return self.jsonfiles
	def getCourseAsMarkdown(self):
		return "todo"
	def getCourseAsHtml(self):
		return "todo"

class EventHandler:
	def onQuitEvent(self, *args):
		Gtk.main_quit(*args)
	def loadCourseByFile(self, *args):
		Gtk.main_quit(*args)
#Class-------------------------------------------------END
#load all .md and .json file into cf
cf = CourseFolder("courses/")

#load userui from .glade file
builder = Gtk.Builder()
builder.add_from_file("ui/userui.glade")
#adding EventHandler class to builder
builder.connect_signals(EventHandler());

window = builder.get_object("main_window")
window.show_all()

#load listbox
tutorials_listbox = builder.get_object("tutorials_listbox")

#build/fill listbox
listTopInfoLabel = Gtk.Label("All Tutorials") #set title of listbox
tutorials_listbox.add(listTopInfoLabel)

#fill tutorials_listbox with all .md files as coursenames
for coursename in cf.getMdFiles():	
	row = Gtk.ListBoxRow()
	hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
	row.add(hbox)
	btn = Gtk.Button(label=coursename.split(".")[0])
	hbox.pack_start(btn, True, True, 0)
	tutorials_listbox.add(row)
#show listbox
tutorials_listbox.show_all()

#get new instion of webkit
wv = WebKit.WebView()

#fill vw with frist .md file in listbox by default
#convert .md to .html
#load .html file in vw 
wv.open("courses/testdata.html")

#addind vw to scrolledWindow
scrolledWindow = builder.get_object("scrolledWindow")
scrolledWindow.add(wv)
scrolledWindow.show_all()

#run gtk.main
Gtk.main()