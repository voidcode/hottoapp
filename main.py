#!/usr/bin/pyhton
from gi.repository import Gtk
import json
from pprint import pprint


with open("tutorials/php101/exams.json") as exams_file:
	exams_data = json.load(exams_file)

pprint(exams_data["php101.md"]["Hvad er php?"])

class EventHandler:
	def onQuitEvent(self, *args):
		Gtk.main_quit(*args)

builder = Gtk.Builder()
builder.add_from_file("ui/userui.glade")
builder.connect_signals(EventHandler());

window = builder.get_object("main_window")
window.show_all()

tutorials_listbox = builder.get_object("tutorials_listbox")

listTopInfoLabel = Gtk.Label("TODO (tutorials)")
tutorials_listbox.add(listTopInfoLabel)

row = Gtk.ListBoxRow()
hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
row.add(hbox)
btn = Gtk.Button(label="php101")
hbox.pack_start(btn, True, True, 0)
tutorials_listbox.add(row)

row = Gtk.ListBoxRow()
hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
row.add(hbox)
btn = Gtk.Button(label="Mysql + php")
hbox.pack_start(btn, True, True, 0)
tutorials_listbox.add(row)

row = Gtk.ListBoxRow()
hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
row.add(hbox)
btn = Gtk.Button(label="Mysql + NodeJs")
hbox.pack_start(btn, True, True, 0)
tutorials_listbox.add(row)


tutorials_listbox.show_all()



tutorials_scrolledwindow = builder.get_object("tutorials_scrolledwindow")
Gtk.main()