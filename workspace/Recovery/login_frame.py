from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import pickle as pk
from assign_frame import AssignFrame
# from user import User
# import my_algorithm

class LoginFrame(Frame):
    """
    def removeEntries(self) -> None: # 모든 엔트리의 필드값을 지우는 메소드
        self.idEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
    """

    """
    def loginUser(self) -> User: # None일 경우 로그인 실패
        userListFile = open(file = '..\\Datas\\user_list.bin', mode = 'rb')
        userList: list[User] = pk.load(file = userListFile)
        userListFile.close()

        id = self.idEntry.get()
        if len(id) == 0:
            messagebox.showwarning('Warning', 'ID를 입력하세요.')
            return None
        index = my_algorithm.binarySearch(userList, 'User', id)
        if index == -1:
            messagebox.showinfo('로그인 실패', '가입되지 않은 ID입니다.')
            return None

        password = self.passwordEntry.get()
        if len(password) == 0:
            messagebox.showwarning('Warning', 'Password를 입력하세요.')
            return None
        if password == userList[index].getPassword():
            return userList[index]
        else:
            messagebox.showinfo('로그인 실패', 'Password가 틀렸습니다.')
            return None
    """

    def openAssignFrame(self) -> None:
        newFrame = Tk()
        newFrame.geometry('800x800')

        assignFrame = AssignFrame(newFrame)
        assignFrame.place(x = 0, y = 0)

        newFrame.mainloop()

    def __init__(self, window: Frame) -> None:
        ############################### 로그인/회원가입 화면 ############################################
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)

        self.loginTitleLabel = Label(window, text = '뇌졸중 예방\n시스템', font = ('Arial', 45, 'bold'), bg = '#09FFFA')
        self.loginTitleLabel.place(x = 250, y = 200)

        self.idLabel = Label(window, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.passwordLabel = Label(window, text = 'Password', font = ('Arial', 15, 'bold'), bg = '#09FFFA')

        self.idEntry = Entry(window, font = ('Arial', 15), width = 25)
        self.passwordEntry = Entry(window, font = ('Arial', 15), show = '●', width = 25)

        self.idLabel.place(x = 200, y = 500); self.idEntry.place(x = 330, y = 500)
        self.passwordLabel.place(x = 200, y = 600); self.passwordEntry.place(x = 330, y = 600)



        self.loginButton = Button(window, text = '로그인', font = ('Arial', 14, 'bold'), bg = 'white',\
                width = 9, activebackground = '#09FFFA', borderwidth = 1)
        self.assignButton = Button(window, text = '회원가입', font = ('Arial', 14, 'bold'), bg = 'white',\
                width = 9, activebackground = '#09FFFA', borderwidth = 1, command = self.openAssignFrame)

        self.loginButton.place(x = 285, y = 700)
        self.assignButton.place(x = 415, y = 700)
        ##########################################################################################################