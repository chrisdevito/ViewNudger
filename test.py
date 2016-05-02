import sys

DIR = ("E:\Users\Chris\Dropbox\Public\Scripts\ViewNudger")
sys.path.insert(1, DIR)

from ViewNudger import ui

if __name__ == '__main__':
    global win

    try:
        win.close()
    except:
        pass

    win = ui.UI()
    win.create()
