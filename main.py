#!/usr/bin/env python
from gi.repository import Gtk, Gdk
import json, os, markdown2
from pprint import pprint

from gi.repository import WebKit
coursesRoot = os.getenv('HOME')+'/.howtoapp-courses'
if not os.path.exists(coursesRoot):
	print 'mkdir --> '+coursesRoot
	os.mkdir(coursesRoot)

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

global mainwindow

mainwindowIsFullscreen = True
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
def loadCourse(coursefilename):
	currentSelectedCourse = coursename
	tmp=''
	with open(os.getenv('HOME') +'/.howtoapp-courses/'+ coursefilename, 'r') as data:
		tmp = data.read()
	#print htmlStartString+markdown2.markdown(tmp)+htmlEndString
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
	global isMainWindowFullscreen
	global currentSelectedCoursename
	def __init__(self):
		self.isMainWindowFullscreen = True
		self.currentSelectedCoursename = ''
	def onQuitEvent(self, *args):
		Gtk.main_quit(*args)
	def showMarkdownEditor(self, coursename):
		builder.add_from_file(os.getcwd() + "/ui/markdowneditor.glade")

		filechooser = builder.get_object('filechooser')
		filechooser.set_filename(os.getenv('HOME') + '/.howtoapp-courses/'+coursename+'.test')

		mdCourseFilePath = os.getenv('HOME') + '/.howtoapp-courses/'+coursename+'.md'

		mdDataBuilder=''
		if os.path.exists(mdCourseFilePath):
			with open(mdCourseFilePath, 'r+') as data:
				mdDataBuilder = data.read()
		else:
			f = open(mdCourseFilePath, 'w+')
			f.write('TEST DATA')
			f.close()
			with open(mdCourseFilePath, 'r') as d:
				mdDataBuilder = d.read() 

		print mdDataBuilder
		#left menu
		h1 = builder.get_object('image_h1')
		h2 = builder.get_object('image_h2')
		h3 = builder.get_object('image_h3')
		h4 = builder.get_object('image_h4')
		h5 = builder.get_object('image_h5')
		bold = builder.get_object('image_bold')
		h1.set_from_file(os.getcwd() + '/images/png/h1.png')
		h2.set_from_file(os.getcwd() + '/images/png/h2.png')
		h3.set_from_file(os.getcwd() + '/images/png/h3.png')
		h4.set_from_file(os.getcwd() + '/images/png/h4.png')
		h5.set_from_file(os.getcwd() + '/images/png/h5.png')
		bold.set_from_file(os.getcwd() + '/images/png/bold.png')
		
		#rigth menu
		hr = builder.get_object('image_hr')
		orderlist = builder.get_object('image_orderlist')
		dotslist = builder.get_object('image_dotslist')		
		codetoggle = builder.get_object('image_codetoggle')
		image = builder.get_object('image_image')

		hr.set_from_file(os.getcwd() + '/images/png/hr.png')
		dotslist.set_from_file(os.getcwd() + '/images/png/dotslist.png')
		orderlist.set_from_file(os.getcwd()+'/images/png/orderlist.png')
		codetoggle.set_from_file(os.getcwd() + '/images/png/code_toggle.png')
		image.set_from_file(os.getcwd() + '/images/png/image.png')
		 

		sw_edit = builder.get_object('sw_edit')
		wv_edit = WebKit.WebView()
		addBrowserSettings(wv_edit)
		wv_edit.open(os.getcwd() + '/markdowneditor.html')

		wv_edit.execute_script("loadMdFile('%s.md');" % coursename)

		sw_edit.add(wv_edit)
		sw_edit.show_all()
		markdowneditor= builder.get_object('markdowneditor_window')
		markdowneditor.override_background_color(0, bgColor)
		markdowneditor.set_position(Gtk.WindowPosition.CENTER)
		markdowneditor.show_all()
	def onBtnNext_newcoursedialog(self, *args):
		label_status = builder.get_object('label_status')
		coursename = builder.get_object('entry_coursename').get_text()
		
		tv_info = builder.get_object('tv_info')
		buf = tv_info.get_buffer()
 		info = buf.get_text(
 			buf.get_start_iter(), 
 			buf.get_end_iter(), 
 			True
 		)
		#--
		if not coursename == '':
			author = builder.get_object('entry_author').get_text()
			testFilePath = coursesRoot+'/'+coursename+'.test'
			print testFilePath
			f = open(testFilePath, 'w+')
			newTestMetaData = {
				'name': coursename,	
				'info': '',
				'author': author,
				'license': ''
			}
			json.dump(newTestMetaData, f, indent=4)
			f.close()
			self.showMarkdownEditor(coursename)
			builder.get_object("newcoursedialog_window").hide()
		else:
			label_status.set_text('You need to add a coursename!!')
	def openNewCourseDialog(self, *args):
		#print 'openNewCourseDialog is clicked!!'
		builder.add_from_file(os.getcwd() + "/ui/newcoursedialog.glade")
		newcoursedialog = builder.get_object("newcoursedialog_window")
		newcoursedialog.set_title('New course')
		newcoursedialog.override_background_color(0, bgColor)
		newcoursedialog.set_position(Gtk.WindowPosition.CENTER)
		newcoursedialog.show_all()
		
		btn_next = builder.get_object('btn_next')
		btn_next.connect('clicked', self.onBtnNext_newcoursedialog)
	def onTutorialsListboxItemClicked(self, btn):
		self.currentSelectedCoursename = btn.get_label().lower()
		loadCourse(btn.get_label().lower()+'.md')
	def onWvLoadFinished(self, frame, s):
		if not self.currentSelectedCoursename is '': 
			courseName = 'skp'
			courseFolder = os.getenv('HOME') +'/.howtoapp-courses/'
			wv.execute_script("loadTest('"+courseFolder+"', '"+self.currentSelectedCoursename+"');")
		else:
			print 'You need to select a coursename! current is-->'+currentSelectedCoursename	
	def onStartExam(self, btn):
		path = os.getcwd()+"/exam.html"
		wv.open(path)
	def toggleFullScreen(self, btn):
		if self.isMainWindowFullscreen is True:
			self.isMainWindowFullscreen = False
			mainwindow.unfullscreen()
		elif self.isMainWindowFullscreen is False:
			self.isMainWindowFullscreen = True
			mainwindow.fullscreen()
#Class-------------------------------------------------END
#load userui from .glade file
builder = Gtk.Builder()
builder.add_from_file(os.getcwd() + "/ui/userui.glade")
#adding EventHandler class to builder
eh = EventHandler()
builder.connect_signals(eh)
#load all .md and .json file into cf
cf = CourseFolder(os.getenv('HOME') +'/.howtoapp-courses')
wv.connect('load-finished', eh.onWvLoadFinished)

mainwindow = builder.get_object("main_window")
mainwindow.set_icon_from_file(os.getcwd() + "/images/logo.svg")
mainwindow.override_background_color(0, bgColor)
mainwindow.set_position(Gtk.WindowPosition.CENTER)

mainwindow.fullscreen()

mainwindow.connect("delete-event", Gtk.main_quit)
mainwindow.show_all()
#load listbox
tutorials_listbox = builder.get_object("tutorials_listbox")

#adding logo
logo = Gtk.Image()
logo.set_from_file(os.getcwd() +'/images/logo.svg')

btnLogo = Gtk.Button()
btnLogo.connect('clicked', eh.toggleFullScreen)
btnLogo.set_image(logo) 
btnLogo.set_relief(Gtk.ReliefStyle.NONE)
logo.override_background_color(0, bgColor)
tutorials_listbox.add(btnLogo)

#build/fill listbox
listTopInfoLabel = Gtk.Label() #set title of listbox
listTopInfoLabel.set_halign(Gtk.Align.START)
listTopInfoLabel.set_markup('<b>All courses:</b>')

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
	hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
	row.add(hbox)	
	mdbtn = Gtk.Button(label=coursename.split(".")[0].title())
	mdbtn.connect("clicked", eh.onTutorialsListboxItemClicked)
			
	jsonbtn = Gtk.Button(label='exam'.title())
	jsonbtn.connect('clicked', eh.onStartExam)

	hbox.pack_start(mdbtn, False, False, 5)	
	hbox.pack_end(jsonbtn, False, False, 0)

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