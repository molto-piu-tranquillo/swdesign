from tkinter import *
from login_frame import LoginFrame
from assign_frame import AssignFrame

import pickle as pk

frame = Tk()
frame.geometry('800x800')

loginFrame = LoginFrame(frame)
loginFrame.pack()

frame.mainloop()