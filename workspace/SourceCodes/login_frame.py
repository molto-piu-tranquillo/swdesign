DEBUG = False

from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import pickle as pk
from assign_frame import AssignFrame
from main_frame import MainFrame
from user import User
# from user import User
# import my_algorithm

class LoginFrame(Frame):
    def hideElements(self): # 로그인 화면의 각종 요소를 숨기는 메소드
        self.loginTitleLabel.place_forget()
        self.idLabel.place_forget(); self.idEntry.place_forget()
        self.passwordLabel.place_forget(); self.passwordEntry.place_forget()
        self.loginButton.place_forget()
        self.assignButton.place_forget()

    def showElements(self): # 로그인 화면의 각종 요소를 표시해주는 메소드
        self.loginTitleLabel.place(x = 250, y = 200)
        self.idLabel.place(x = 200, y = 500); self.idEntry.place(x = 330, y = 500)
        self.passwordLabel.place(x = 200, y = 600); self.passwordEntry.place(x = 330, y = 600)
        self.loginButton.place(x = 285, y = 700); self.assignButton.place(x = 415, y = 700)

    def openAssignFrame(self) -> None:
        # self.hideElements()
        self.assignFrame = AssignFrame(self)
        self.assignFrame.place(x = 0, y = 0)

    def closeAssignFrame(self) -> None:
        self.assignFrame.place_forget()

        self.showElements()

    def __init__(self, window: Frame) -> None:
        ############################### 로그인/회원가입 화면 ############################################
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)

        self.loginTitleLabel = Label(self, text = '뇌졸중 예방\n시스템', font = ('Arial', 45, 'bold'), bg = '#09FFFA')
        self.loginTitleLabel.place(x = 250, y = 200)

        self.idLabel = Label(self, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.passwordLabel = Label(self, text = 'Password', font = ('Arial', 15, 'bold'), bg = '#09FFFA')

        self.idEntry = Entry(self, font = ('Arial', 15), width = 25)
        self.passwordEntry = Entry(self, font = ('Arial', 15), show = '●', width = 25)

        self.idLabel.place(x = 200, y = 500); self.idEntry.place(x = 330, y = 500)
        self.passwordLabel.place(x = 200, y = 600); self.passwordEntry.place(x = 330, y = 600)



        self.loginButton = Button(self, text = '로그인', font = ('Arial', 14, 'bold'), bg = 'white',\
                width = 9, activebackground = '#09FFFA', borderwidth = 1, command = lambda: self.login())
        self.assignButton = Button(self, text = '회원가입', font = ('Arial', 14, 'bold'), bg = 'white',\
                width = 9, activebackground = '#09FFFA', borderwidth = 1, command = self.openAssignFrame)

        self.loginButton.place(x = 285, y = 700)
        self.assignButton.place(x = 415, y = 700)
        ##########################################################################################################

    def login(self): # 로그인 성공 시 메인 프레임을 보여줌.
        if len(self.idEntry.get()) == 0:
            messagebox.showerror('오류', 'ID가 입력되지 않았습니다.')
            return
        if len(self.passwordEntry.get()) == 0:
            messagebox.showerror('오류', '비밀번호가 입력되지 않았습니다.')
            return

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        if len(userlist) == 0:
            messagebox.showinfo('알림', 'ID/PW가 일치하지 않습니다.')
            return
        for i in range(len(userlist)):
            if userlist[i].getId() == self.idEntry.get() and userlist[i].getPw() == self.passwordEntry.get():
                self.__loginedUser = userlist[i]
                break
            if i == len(userlist) - 1:
                messagebox.showinfo('알림', 'ID/PW가 일치하지 않습니다.')
                return

        self.mainFrame = MainFrame(self, self.__loginedUser)
        self.mainFrame.place(x = 0, y = 0)



if DEBUG:
    window = Tk()
    window.geometry('800x800')

    frame = LoginFrame(window)
    frame.place(x = 0, y = 0)

    window.mainloop()