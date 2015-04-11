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
#Class-------------------------------------------------START
class EventHandler:
	def onQuitEvent(self, *args):
		Gtk.main_quit(*args)

class CourseFolder:
	def load(self, filetype):
		coursefiles = [];
		coursepath = "courses/"
		for name in os.listdir(coursepath):
			if name.split(".")[-1] == filetype and os.path.isfile(os.path.join(coursepath, name)):
				coursefiles.append(name)
		return coursefiles;
#Class-------------------------------------------------END
print CourseFolder().load("json")

print CourseFolder().load("md")



builder = Gtk.Builder()
builder.add_from_file("ui/userui.glade")
builder.connect_signals(EventHandler());

window = builder.get_object("main_window")
window.show_all()

tutorials_listbox = builder.get_object("tutorials_listbox")

listTopInfoLabel = Gtk.Label("All Tutorials")
tutorials_listbox.add(listTopInfoLabel)

#fill tutorials_listbox with all .md files as coursenames
for coursename in CourseFolder().load("md"):	
	row = Gtk.ListBoxRow()
	hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
	row.add(hbox)
	btn = Gtk.Button(label=coursename.split(".")[0])
	hbox.pack_start(btn, True, True, 0)
	tutorials_listbox.add(row)

tutorials_listbox.show_all()



wv = WebKit.WebView()
wv.open("courses/testdata.html")

#addind webkit to scrolledWindow
scrolledWindow = builder.get_object("scrolledWindow")
scrolledWindow.add(wv)
scrolledWindow.show_all()


Gtk.main()