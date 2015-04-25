#!/usr/bin/env python
from gi.repository import Gtk, Gdk
import json, os, markdown2
from pprint import pprint

from gi.repository import WebKit

def addBrowserSettings(wvObj):
	browserSettings = wvObj.get_settings()
	browserSettings.set_property("enable-java-applet", False)
	browserSettings.set_property("enable-plugins", True)
	browserSettings.set_property("enable-scripts", True)
	browserSettings.set_property("enable-private-browsing", False)
	browserSettings.set_property("enable-spell-checking", False)
	browserSettings.set_property('enable-file-access-from-file-uris', 1)
	browserSettings.set_property("enable-dns-prefetching", True)
	browserSettings.set_property("enable-webaudio", True)
	browserSettings.set_property("enable-webgl", True)
	browserSettings.set_property("enable-fullscreen", True)
	browserSettings.set_property("enable-xss-auditor", True)
	browserSettings.set_property("javascript-can-open-windows-automatically", True)
	browserSettings.set_property('user-agent', 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')

#get new instion of webkit
wv = WebKit.WebView()
addBrowserSettings(wv)

#wv.execute_script("alert('ddd');")
#build html vars with stylesheet-link
cssLinkTag = "<link rel=\"stylesheet\" type=\"text/css\" href=\""+ os.getcwd() + "/css/desktop.css\">"
htmlStartString = "<!DOCTYPE html><html><head>"+cssLinkTag+"<meta charset=\"UTF-8\"></head><body>"
htmlEndString = "</body></html>"


bgColor = Gdk.RGBA.from_color(Gdk.color_parse('#141414'))
#Class-------------------------------------------------STARTs
#this class load all course file into class vars
currentSelectedCourse=''
def loadCourse(coursefilename):
	tmp=''
	with open(os.getcwd() + "/courses/"+ coursefilename, 'r') as data:
		tmp = data.read()
	#print htmlStartString+markdown2.markdown(tmp)+htmlEndString
	wv.load_html_string(htmlStartString+markdown2.markdown(tmp)+htmlEndString, "file:///")

class CourseFolder:
	global currentSelectedCourse;
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
	def showMarkdownEditor(self, *args):
		builder.add_from_file(os.getcwd() + "/ui/markdowneditor.glade")
		#left menu
		h1 = builder.get_object('image_h1')
		h2 = builder.get_object('image_h2')
		h3 = builder.get_object('image_h3')
		h4 = builder.get_object('image_h4')
		h5 = builder.get_object('image_h5')
		p = builder.get_object('image_p')
		h1.set_from_file(os.getcwd() + '/images/png/h1.png')
		h2.set_from_file(os.getcwd() + '/images/png/h2.png')
		h3.set_from_file(os.getcwd() + '/images/png/h3.png')
		h4.set_from_file(os.getcwd() + '/images/png/h4.png')
		h5.set_from_file(os.getcwd() + '/images/png/h5.png')
		p.set_from_file(os.getcwd() + '/images/png/p.png')


		sw_edit = builder.get_object('sw_edit')
		wv_edit = WebKit.WebView()
		addBrowserSettings(wv_edit)
		wv_edit.open(os.getcwd() + '/markdowneditor.html')
		sw_edit.add(wv_edit)
		sw_edit.show_all()
		markdowneditor= builder.get_object('markdowneditor_window')
		markdowneditor.override_background_color(0, bgColor)
		markdowneditor.set_position(Gtk.WindowPosition.CENTER)
		markdowneditor.show_all()
	def openNewCourseDialog(self, *args):
		#print 'openNewCourseDialog is clicked!!'
		builder.add_from_file(os.getcwd() + "/ui/newcoursedialog.glade")
		newcoursedialog = builder.get_object("newcoursedialog_window")
		builder.connect_signals(self)
		newcoursedialog.set_title('New course / edit course')
		newcoursedialog.override_background_color(0, bgColor)
		newcoursedialog.set_position(Gtk.WindowPosition.CENTER)
		newcoursedialog.show_all()
	def onTutorialsListboxItemClicked(self, btn):
		currentSelectedCourse = btn.get_label()+".md"
		loadCourse(btn.get_label()+".md")
	def onTaskExam(self, *args):
		#print("onTaskExam is clicked!!")
		uriPath = os.getcwd()+"/exam.html"
		#% btn.get_label()
		#examHtmlBuilder=''
		#with open(uriPath, 'r') as data:
			#examHtmlBuilder = data.read()
		#wv.load_html_string(examHtmlBuilder, 'file:///')
		wv.open(uriPath)
		#print("wv.load --> os.getcwd()+ /exam.html")
		#print("We try this url: " +uriPath)
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
mainwindow.override_background_color(0, bgColor)
mainwindow.set_position(Gtk.WindowPosition.CENTER)
#mainwindow.fullscreen()
mainwindow.show_all()
#load listbox
tutorials_listbox = builder.get_object("tutorials_listbox")

#build/fill listbox
listTopInfoLabel = Gtk.Label() #set title of listbox
listTopInfoLabel.set_markup('<b>CourseFolder</b>')

#set bgcolor
tutorials_listbox.override_background_color(0, bgColor)
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

	hbox.pack_start(btn, True, True, 50)
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