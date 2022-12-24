from tkinter import *
from tkinter.ttk import *
from time import strftime

root = Tk()
root.title("CLOCK")

def Time():
    string = strftime('%I:%M:%S %p')
    label.config(text = string)
    label.after(1000, Time)

label = Label(root, font = ("Times", 70), background = "black", foreground = "white")
label.pack(anchor = 'center')
Time()

mainloop()