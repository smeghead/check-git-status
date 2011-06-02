#!/usr/bin/python
import os, sys
import threading
import gtk
import egg.trayicon     # egg == python-gnome2-extras
import gitutils

DIRNAME = os.path.dirname(__file__)
ICONS = {}
for f in ['__', 'C_', '_U', 'CU']:
    ICONS[f] = '%s/%s.png' % (DIRNAME, f)

'''
extended menu item.
'''
class RepogitoryItemMenu(gtk.ImageMenuItem):
    repo = None
    def __init__(self, name, r):
        gtk.ImageMenuItem.__init__(self, name)
        self.repo = r
        self.set_image(
                gtk.image_new_from_file(ICONS[r['flag']]))
        self.set_tooltip_text((r['path'] + "\n" + r['status']))
        #when menu item is selected, open gnome-terminal in repogitory directory.
        self.connect("activate",
                lambda x: os.popen(
                    '%s --working-directory="%s"' % ('gnome-terminal', self.repo['path'])))

if len(sys.argv) == 1:
    exit('ERROR: required argument search path.')

searchPathes = sys.argv[1:]
trayIconImage = os.path.dirname(__file__) + '/icon.png'

gtk.gdk.threads_init() # This needs to work threading.Timer with gtk.main.

repos = []

timer = None

def updateRepos():
    global repos, timer
    repos = gitutils.searchRepogitoryInfosByPathes(searchPathes, lambda x: True)
    timer = threading.Timer(60, updateRepos)
    timer.start()

updateRepos()

def trayIconClicked(widget, event):
    global repos
    menu = gtk.Menu()
    for r in repos:
        menuitem_x = RepogitoryItemMenu(r['menuItem'], r)
        menu.append(menuitem_x)
    menu.append(gtk.SeparatorMenuItem())
    menuitem_exit = gtk.MenuItem("Exit")
    menu.append(menuitem_exit)
    menuitem_exit.connect("activate", lambda x: timer.cancel() or gtk.main_quit())
    menu.show_all()
    menu.popup(None, None, None, event.button, event.time, tray)

tray = egg.trayicon.TrayIcon("TrayIcon")
box = gtk.EventBox()
img = gtk.Image()
img.set_from_file(trayIconImage)
box.add(img)
tray.add(box)
tray.show_all()

box.connect("button-press-event", trayIconClicked)

gtk.main()

# vim: set ts=4 sw=4 sts=4 expandtab fenc=utf-8:
