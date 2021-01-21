from tkinter import *
import threading
from tkinter import ttk

class progress:
    def __init__(self, parent, func):
        self.toplevel = Toplevel(parent)
        self.progressbar = ttk.Progressbar(self.toplevel, orient = HORIZONTAL, mode = 'indeterminate')
        self.progressbar.pack()
        # self.running = threading.Event()
        # self.running.set()
        self.t = threading.Thread(target=func, args=())
        # self.t.__init__(target = self.progressbar.start, args = ())
        self.t.start()
        #if self.t.isAlive() == True:
        #       print 'worked'
        self.progressbar.after(5000, func=self.end)

    def end(self):
        if self.t.is_alive() == False:
            self.progressbar.stop()
            self.toplevel.destroy()
            self.t.join()