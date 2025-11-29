from tkinter import *
from login_frame import LoginFrame
from assign_frame import AssignFrame

import pickle as pk

frame = Tk()
frame.geometry('800x800')

loginFrame = LoginFrame(frame)
loginFrame.pack()

"""
userlist = []
userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
pk.dump(file = userlistFile, obj = userlist)
userlistFile.close()

assignFrame = AssignFrame(frame)
assignFrame.pack()
"""

frame.mainloop()