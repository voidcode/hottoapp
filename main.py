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

wv_edit = WebKit.WebView()
addBrowserSettings(wv_edit)

#wv.execute_script("alert('ddd');")
#build html vars with stylesheet-link
css = "<link rel=\"stylesheet\" type=\"text/css\" href=\""+ os.getcwd() + "/css/desktop.css\"><link rel=\"stylesheet\" type=\"text/css\" href=\""+ os.getcwd() + "/css/course.css\">"
jsJq = "<script type=\"text/javascript\" src=\""+os.getcwd()+"/js/jquery-1.11.2.min.js\"></script>"
jsDefault = "<script type=\"text/javascript\" src=\""+os.getcwd()+"/js/default.js\"></script>"
htmlStartString = "<!DOCTYPE html><html><head>"+css+"<meta charset=\"UTF-8\"></head><body>"
htmlEndString = jsJq+jsDefault+"</body></html>"


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
	print htmlStartString+markdown2.markdown(tmp)+htmlEndString
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
	def onInsertTag(self, args, tagname):
		wv_edit.execute_script('insertTag("%s");' % tagname)
	def codeToogleView(self, *args):
		print 'ToggleCodeView'
	def onShowAbortDialog(self, *args):
		abortdialog = builder.add_from_file(os.getcwd() + '/ui/abort.glade')
		#sw_rigth.add(abortdialog)
		#.show_all()
	def showMarkdownEditor(self, coursename):
		builder.add_from_file(os.getcwd() + "/ui/markdowneditor.glade")

		filechooser = builder.get_object('filechooser')
		filechooser.set_filename(os.getenv('HOME') + '/.howtoapp-courses/'+coursename+'.md')

		mdCourseFilePath = os.getenv('HOME') + '/.howtoapp-courses/'+coursename+'.md'

		mdDataBuilder=''
		if os.path.exists(mdCourseFilePath):
			with open(mdCourseFilePath, 'r+') as data:
				mdDataBuilder = data.read()
		else:
			f = open(mdCourseFilePath, 'w+')
			f.write('<h1>'+coursename+'</h1>')
			f.close()
			with open(mdCourseFilePath, 'r') as d:
				mdDataBuilder = d.read() 
		#left menu
		#h1 = builder.get_object('image_h1')
		#h2 = builder.get_object('image_h2')
		#h3 = builder.get_object('image_h3')
		#h4 = builder.get_object('image_h4')
		#h5 = builder.get_object('image_h5')
		#h1.set_from_file(os.getcwd() + '/images/png/h1.png')
		#h2.set_from_file(os.getcwd() + '/images/png/h2.png')
		#h3.set_from_file(os.getcwd() + '/images/png/h3.png')
		#h4.set_from_file(os.getcwd() + '/images/png/h4.png')
		
		#h5.set_from_file(os.getcwd() + '/images/png/h5.png')




		#rigth menu

		#hr = builder.get_object('image_hr')
		#orderlist = builder.get_object('image_orderlist')
		#dotslist = builder.get_object('image_dotslist')		
		#codetoggle = builder.get_object('image_codetoggle')
		#image = builder.get_object('image_image')

		#hr.set_from_file(os.getcwd() + '/images/png/hr.png')
		#dotslist.set_from_file(os.getcwd() + '/images/png/dotslist.png')
		#orderlist.set_from_file(os.getcwd()+'/images/png/orderlist.png')
		#codetoggle.set_from_file(os.getcwd() + '/images/png/code_toggle.png')
		#image.set_from_file(os.getcwd() + '/images/png/image.png')

		sw_edit = builder.get_object('sw_edit')


		rigthBox = builder.get_object('rigthBox')
		rigthBox.override_background_color(0, bgColor)
		rigthHbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

		#H1
		h1Img = Gtk.Image()
		h1Img.set_from_file(os.getcwd() + '/images/png/h1.png')
		h1Bold = Gtk.Button()
		h1Bold.set_image(h1Img)
		h1Bold.connect('clicked', self.onInsertTag, 'h1')
		rigthHbox.add(h1Bold)

		#H2
		h2Img = Gtk.Image()
		h2Img.set_from_file(os.getcwd() + '/images/png/h2.png')
		h2Bold = Gtk.Button()
		h2Bold.set_image(h2Img)
		h2Bold.connect('clicked', self.onInsertTag, 'h2')
		rigthHbox.add(h2Bold)

		#H3
		h3Img = Gtk.Image()
		h3Img.set_from_file(os.getcwd() + '/images/png/h3.png')
		h3Bold = Gtk.Button()
		h3Bold.set_image(h3Img)
		h3Bold.connect('clicked', self.onInsertTag, 'h3')
		rigthHbox.add(h3Bold)

		#Blod
		boldImg = Gtk.Image()
		boldImg.set_from_file(os.getcwd() + '/images/png/bold.png')
		btnBold = Gtk.Button()
		btnBold.set_image(boldImg)
		btnBold.connect('clicked', self.onInsertTag, 'b')
		rigthHbox.add(btnBold)

		#p
		pImg = Gtk.Image()
		pImg.set_from_file(os.getcwd() + '/images/png/p.png')
		btnP = Gtk.Button()
		btnP.set_image(pImg)
		btnP.connect('clicked', self.onInsertTag, 'p')
		rigthHbox.add(btnP)
	
		#camera
		cameraImg = Gtk.Image()
		cameraImg.set_from_file(os.getcwd() + '/images/png/image.png')
		btnCamera = Gtk.Button()
		btnCamera.set_image(cameraImg)
		btnCamera.connect('clicked', self.onInsertTag, 'a')
		rigthHbox.add(btnCamera)

		#orderlist
		orderlistImg = Gtk.Image()
		orderlistImg.set_from_file(os.getcwd() + '/images/png/orderlist.png')
		orderlistBold = Gtk.Button()
		orderlistBold.set_image(orderlistImg)
		orderlistBold.connect('clicked', self.onInsertTag, 'ol')
		rigthHbox.add(orderlistBold)

		#dotslist
		dotslistImg = Gtk.Image()
		dotslistImg.set_from_file(os.getcwd() + '/images/png/dotslist.png')
		dotslistBold = Gtk.Button()
		dotslistBold.set_image(dotslistImg)
		dotslistBold.connect('clicked', self.onInsertTag, 'ul')
		rigthHbox.add(dotslistBold)

		#br
		brImg = Gtk.Image()
		brImg.set_from_file(os.getcwd() + '/images/svg/br.svg')
		btnBr = Gtk.Button()
		btnBr.set_image(brImg)
		btnBr.connect('clicked', self.onInsertTag, 'br')
		rigthHbox.add(btnBr)

		#code view
		#codeImg = Gtk.Image()
		#codeImg.set_from_file(os.getcwd() + '/images/png/code_toggle.png')
		#btnCode = Gtk.Button()
		#btnCode.set_image(codeImg)
		#btnCode.connect('clicked', self.codeToogleView)
		#rigthHbox.add(btnCode)

		#add leftHbox to leftBox
		rigthBox.add(rigthHbox)

		wv_edit.connect('load-finished', self.onWvLoadFinished)
		wv_edit.open(os.getcwd() + '/markdowneditor.html')
		wv_edit.execute_script("loadMdFiles('"+os.getenv('HOME')+"', '"+coursename+".md');" )

		sw_edit.add(wv_edit)
		sw_edit.show_all()
		markdowneditor= builder.get_object('markdowneditor_window')
		markdowneditor.override_background_color(0, bgColor)
		markdowneditor.set_position(Gtk.WindowPosition.CENTER)
		markdowneditor.show_all()

		btn_show_addquestionsdialog = builder.get_object('btn_show_addquestionsdialog')
		btn_show_addquestionsdialog.connect('clicked', self.btn_show_addquestionsdialog)

	def btn_show_addquestionsdialog(self, *args):
		builder.add_from_file(os.getcwd() + "/ui/addquestionsdialog.glade")


		scrolledwindow_alladdedcourse = builder.get_object('scrolledwindow_alladdedcourse')
		wv_alladdedcourse = WebKit.WebView()
		addBrowserSettings(wv_alladdedcourse)
		wv_alladdedcourse.open(os.getcwd()+'/addquestions.html')
		scrolledwindow_alladdedcourse.add(wv_alladdedcourse)


		btn_new_question_item = builder.get_object('btn_new_question_item')
		plusImg = Gtk.Image()
		plusImg.set_from_file(os.getcwd() + '/images/png/plus.png')
		btn_new_question_item.set_image(plusImg)

		addquestionsdialog = builder.get_object('window_addquestionsdialog')
		addquestionsdialog.set_title('Add questions')
		addquestionsdialog.set_position(Gtk.WindowPosition.CENTER)
		addquestionsdialog.override_background_color(0, bgColor)
		addquestionsdialog.show_all()
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
			testFilePath = coursesRoot+'/'+coursename+'.test'
			if not os.path.exists(testFilePath):
				author = builder.get_object('entry_author').get_text()
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
				label_status.set_text('Please try an other coursename.\n('+coursename+') do already exists!')
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
			wv.execute_script("loadMdFiles('"+courseFolder+"', '"+self.currentSelectedCoursename+"');")
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
	def pageScrollUp(self, *args):
		wv.execute_script('pageScrollDown')
		wv_edit.execute_script('pageScrollDown')
	def pageScrollDown(self, *args):
		wv.execute_script('pageScrollDown')
		wv_edit.execute_script('pageScrollDown')
#Class-------------------------------------------------END
#load userui from .glade file
builder = Gtk.Builder()
builder.add_from_file(os.getcwd() + "/ui/userui.glade")

#adding EventHandler class to builder
eh = EventHandler()
builder.connect_signals(eh)


startExamImg = Gtk.Image()
startExamImg.set_from_file(os.getcwd()+'/images/svg/stopwatch6.svg')
btn_startexam = builder.get_object('btn_startexam')
btn_startexam.set_image(startExamImg)

#load all .md and .json file into cf
cf = CourseFolder(os.getenv('HOME') +'/.howtoapp-courses')
wv.connect('load-finished', eh.onWvLoadFinished)

mainwindow = builder.get_object("main_window")
mainwindow.set_icon_from_file(os.getcwd() + "/images/logo.svg")
mainwindow.override_background_color(0, bgColor)
mainwindow.set_position(Gtk.WindowPosition.CENTER)
mainwindow.fullscreen()
mainwindow.connect("delete-event", Gtk.main_quit)

#set btn_scrolldown
scrolldownImg = Gtk.Image()
scrolldownImg.set_from_file(os.getcwd()+'/images/svg/down_arrow.svg')
btn_scrolldown = builder.get_object('btn_scrolldown')
btn_scrolldown.connect('clicked', eh.pageScrollDown)
btn_scrolldown.set_image(scrolldownImg)

#set btn_scrollup
scrollupImg = Gtk.Image()
scrollupImg.set_from_file(os.getcwd()+'/images/svg/up_arrow.svg')
btn_scrollup = builder.get_object('btn_scrollup')
btn_scrollup.connect('clicked', eh.pageScrollUp)
btn_scrollup.set_image(scrollupImg)

mainwindow.show_all()


box_left = builder.get_object('main_paned')
box_left.override_background_color(0, bgColor)

#adding logo
logo = Gtk.Image()
logo.set_from_file(os.getcwd() +'/images/logo.svg')

btnLogo = builder.get_object('btnlogo')
btnLogo.connect('clicked', eh.toggleFullScreen)
btnLogo.set_image(logo) 
#btnLogo.set_relief(Gtk.ReliefStyle.NONE)
#logo.override_background_color(0, bgColor)

sw_left = builder.get_object("sw_left")
#load listbox
listbox = Gtk.ListBox()
sw_left.add(listbox)

#set bgcolor
listbox.add(btnLogo)
listbox.set_selection_mode(Gtk.SelectionMode.NONE)
listbox.override_background_color(0, bgColor)

hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

#fill tutorials_listbox with all .md files as coursenamses
fristRun = True
for coursename in cf.getMdFiles():
	#only load frist course
	if fristRun==True:
		#eh.currentSelectedCoursename = coursename
		loadCourse(coursename)
		fristRun=False
	row = Gtk.ListBoxRow()

	#hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
	mdbtn = Gtk.Button(label=coursename.split(".")[0].title())
	mdbtn.connect("clicked", eh.onTutorialsListboxItemClicked)
	mdbtn.set_size_request(20, 40)
	row.add(mdbtn)
	listbox.add(row)
#show listbox
listbox.add(hbox)
listbox.show_all()

		#fill vw with frist .md file in listbox by default
		#convert .md to .html
		#load .html file in vw 

#addind vw to sv_rigth
sw_rigth = builder.get_object("sw_rigth")
sw_rigth.add(wv)
sw_rigth.show_all()
#run gtk.main
Gtk.main()