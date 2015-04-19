#!/usr/bin/env python
from gi.repository import Gtk
import json, os, markdown2
from pprint import pprint

from gi.repository import WebKit
with open("courses/php101.json") as coursefile:
	course = json.load(coursefile)

pprint("Title: "+course["name"].split(".")[-1])
pprint("File: "+course["file"])

# exams->test0->quition1->choice
pprint(course["exams"][0][1]["choice"])

pprint(course["exams"][0][1]["answer"])

#get new instion of webkit
wv = WebKit.WebView()
browserSettings = wv.get_settings()
browserSettings.set_property("enable-java-applet", False)
browserSettings.set_property("enable-plugins", True)
browserSettings.set_property("enable-scripts", True)
 
browserSettings.set_property("enable-file-access-from-file-uris", True)
 
#browserSettings.set_property("enable-private-browsing", False)
#browserSettings.set_property("enable-spell-checking", False)
#browserSettings.set_property("enable-universal-access-from-file-uris", True)
#browserSettings.set_property("enable-dns-prefetching", True)
browserSettings.set_property("enable-webaudio", True)
browserSettings.set_property("enable-webgl", True)
browserSettings.set_property("enable-fullscreen", True)
#browserSettings.set_property("enable-xss-auditor", False)
browserSettings.set_property("javascript-can-open-windows-automatically", True)
browserSettings.set_property('user-agent', 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')

#wv.execute_script("alert('ddd');")
#build html vars with stylesheet-link
cssLinkTag = "<link rel=\"stylesheet\" type=\"text/css\" href=\""+ os.getcwd() + "/css/desktop.css\">"
htmlStartString = "<!DOCTYPE html><html><head>"+cssLinkTag+"<meta charset=\"UTF-8\"></head><body>"
htmlEndString = "</body></html>"
#Class-------------------------------------------------STARTs
#this class load all course file into class vars
currentSelectedCourse=''
def loadCourse(coursefilename):
	tmp=''
	with open(os.getcwd() + "/courses/"+ coursefilename, 'r') as data:
		tmp = data.read()
	print htmlStartString+markdown2.markdown(tmp)+htmlEndString
	wv.load_html_string(htmlStartString+markdown2.markdown(tmp)+htmlEndString, "file:///")

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
		dialog = Gtk.GtkFileChooserDialog()
		dialog.show_all()
	def openNewCourseDialog(self, *args):
		print 'openNewCourseDialog is clicked!!'
		builder.add_from_file(os.getcwd() + "/ui/newcoursedialog.glade")
		newcoursedialog_window = builder.get_object("newcoursedialog_window")
		newcoursedialog_window.show_all()
	def onTutorialsListboxItemClicked(self, btn):
		currentSelectedCourse = btn.get_label()+".md"
		loadCourse(btn.get_label()+".md")

#Class-------------------------------------------------END

#load userui from .glade file
builder = Gtk.Builder()
builder.add_from_file(os.getcwd() + "/ui/userui.glade")
#adding EventHandler class to builder
eh = EventHandler()
builder.connect_signals(eh)
#load all .md and .json file into cf
cf = CourseFolder("courses/")

mainwindow = builder.get_object("main_window")
mainwindow.set_icon_from_file(os.getcwd() + "/images/logo.svg")
mainwindow.show_all()
#load listbox
tutorials_listbox = builder.get_object("tutorials_listbox")

#build/fill listbox
listTopInfoLabel = Gtk.Label("Courses") #set title of listbox
tutorials_listbox.add(listTopInfoLabel)

#fill tutorials_listbox with all .md files as coursenamses
fristRun = True
for coursename in cf.getMdFiles():
	#only load frist course
	if fristRun==True:
		loadCourse(coursename)
		fristRun=False

	row = Gtk.ListBoxRow()
	hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
	row.add(hbox)
	btn = Gtk.Button(label=coursename.split(".")[0])
	btn.connect("clicked", eh.onTutorialsListboxItemClicked)
	
	#adding course-image
	base = Gtk.Image()
	base.new_from_file(os.getcwd()+ "/courses/base.svg")
	btn.set_image(base)

	hbox.pack_start(btn, True, True, 0)
	tutorials_listbox.add(row)
#show listbox
tutorials_listbox.show_all()


#fill vw with frist .md file in listbox by default
#convert .md to .html
#load .html file in vw 


#addind vw to scrolledWindow
scrolledWindow = builder.get_object("scrolledWindow")
scrolledWindow.add(wv)
scrolledWindow.show_all()



#run gtk.main
Gtk.main()