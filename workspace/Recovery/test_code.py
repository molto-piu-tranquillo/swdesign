from tkinter import *
from login_frame import LoginFrame
from assign_frame import AssignFrame

import pickle as pk

frame = Tk()
frame.geometry('800x800')

loginFrame = LoginFrame(frame)
loginFrame.pack()

# dummy_user = Patient {"Kim", 35, "남", "123", "pw", "010-0000-0000", "test@mail.com", "개인 사용자"}

"""
userlist = []
userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
pk.dump(file = userlistFile, obj = userlist)
userlistFile.close()

assignFrame = AssignFrame(frame)
assignFrame.pack()
"""

frame.mainloop()