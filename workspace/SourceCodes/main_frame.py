from tkinter import *
from SourceCodes.login_frame import LoginFrame
from SourceCodes.assign_frame import AssignFrame

mainFrame = Tk()
mainFrame.geometry('800x800')

loginFrame = LoginFrame()
assignFrame = AssignFrame()

mainFrame.mainloop()