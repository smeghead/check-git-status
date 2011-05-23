#!/usr/bin/python
import os, sys
import gtk
import egg.trayicon     # egg == python-gnome2-extras
import gitutils

'''
extended menu item.
'''
class RepogitoryItemMenu(gtk.ImageMenuItem):
    repo = None
    def __init__(self, name, r):
        gtk.ImageMenuItem.__init__(self, name)
        self.repo = r
        self.set_image(
                gtk.image_new_from_file('%s/%s.png' % (os.path.dirname(__file__), self.repo['flag'])))
        self.connect("activate", lambda x: os.popen('%s --working-directory="%s"' % ('gnome-terminal', self.repo['path'])))

if len(sys.argv) == 1:
    exit('ERROR: required argument search path.')

searchPathes = sys.argv[1:]
trayIconImage = os.path.dirname(__file__) + '/icon.png'

def callback(widget, event):
    repos = gitutils.searchRepogitoryInfosByPathes(searchPathes, lambda x: True)
    menu = gtk.Menu()
    tooltips = gtk.Tooltips()
    tooltips.enable()
    tooltips.set_delay(100)
    for r in repos:
        menuitem_x = RepogitoryItemMenu(r['menuItem'], r)
        tooltips.set_tip(menuitem_x, r['path'] + "\n" + r['status'])
        menu.append(menuitem_x)
    menuitem_exit = gtk.MenuItem("Exit")
    menu.append(menuitem_exit)
    menuitem_exit.connect("activate", lambda x: gtk.main_quit())
    menu.show_all()
    menu.popup(None, None, None, event.button, event.time, tray)

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
