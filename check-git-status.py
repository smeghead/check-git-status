#!/usr/bin/python
import os
import gtk
import egg.trayicon     # egg == python-gnome2-extras


trayIconImage = os.path.dirname(__file__) + '/icon.png'
print trayIconImage

def callback(widget, ev):
    print "Button %i pressed!" % ev.button

tray = egg.trayicon.TrayIcon("TrayIcon")
box = gtk.EventBox()
img = gtk.Image()
img.set_from_file(trayIconImage)
box.add(img)
tray.add(box)
tray.show_all()

box.connect("button-press-event", callback)

gtk.main()

# vim: set ts=4 sw=4 sts=4 expandtab fenc=utf-8:
