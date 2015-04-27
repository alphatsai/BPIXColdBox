#!/usr/bin/python
from Tkinter import *
 
class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
 
    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText["text"] = "Input:"
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=6)
 
        self.outputText = Label(self)
        self.outputText["text"] = "Output:"
        self.outputText.grid(row=1, column=0)
        self.outputField = Entry(self)
        self.outputField["width"] = 50
        self.outputField.grid(row=1, column=1, columnspan=6)
         
        self.new = Button(self)
        self.new["text"] = "New"
        self.new.grid(row=2, column=0)
        self.load = Button(self)
        self.load["text"] = "Load"
        self.load.grid(row=2, column=1)
        self.save = Button(self)
        self.save["text"] = "Save"
        self.save.grid(row=2, column=2)
        self.encode = Button(self)
        self.encode["text"] = "Encode"
        self.encode.grid(row=2, column=3)
        self.decode = Button(self)
        self.decode["text"] = "Decode"
        self.decode.grid(row=2, column=4)
        self.clear = Button(self)
        self.clear["text"] = "Clear"
        self.clear.grid(row=2, column=5)
        self.copy = Button(self)
        self.copy["text"] = "Copy"
        self.copy.grid(row=2, column=6)
 
        self.displayText = Label(self)
        self.displayText["text"] = "something happened"
        self.displayText.grid(row=3, column=0, columnspan=7)
 
if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop() 


#from Tkinter import *
#
#class Application(Frame):
#    def say_hi(self):
#        self.outputstring += "Hi! "
#        print self.outputstring
#
#    def say_two(self):
#        self.outputstring += "Two "
#        print self.outputstring
#
#    def createWidgets(self):
#        self.QUIT = Button(self, fg="Red")
#        self.QUIT["text"] = "QUIT"
#        self.QUIT["fg"]   = "Red"
#        self.QUIT["command"] =  self.quit
#        self.QUIT.pack({"side": "left"})
#
#        self.hi_there = Button(self)
#        self.hi_there["text"] = "Hello",
#        self.hi_there["command"] = self.say_hi
#        self.hi_there.pack({"side":"left"})
#
#        self.add_two = Button(self)
#        self.add_two["text"] = "Two"
#        self.add_two["command"] = self.say_two
#        self.add_two.pack({"side": "left"})
#
#    def __init__(self, master=None):
#        Frame.__init__(self, master, background="white")
#        self.pack()
#        self.createWidgets()
#        self.outputstring = ""
#
#root = Tk()
#root.geometry("500x500+300+300") 
#app = Application(master=root)
#app.mainloop()
#root.destroy()

