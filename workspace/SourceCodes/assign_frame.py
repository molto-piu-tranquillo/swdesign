from tkinter import *
from tkinter import messagebox
import pickle as pk

from user import *

class AssignFrame(Frame):
    """
    def removeEntries(self) -> None: # 모든 엔트리의 필드값을 지우는 메소드
        self.nameEntry.delete(0, END)
        self.emailEntry.delete(0, END)
        self.idEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        self.passwordEntry2.delete(0, END)
        self.schoolEntry.delete(0, END)
        self.gradeEntry.delete(0, END)
    """

    def assignUser(self) -> None:
        userlistFile = open(file = '..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        assignedName = self.nameEntry.get()
        assignedAge = int(self.ageEntry.get())
        assignedGender = self.genderEntry.get()
        assignedId = self.idEntry.get()
        assignedPw = self.pwEntry.get()
        assignedPhoneNumber = self.phoneNumberEntry.get()
        assignedEmail = self.emailEntry.get()

        if self.userTypeEntry.cget('text') == '개인 사용자':
            userlist.append(Patient(assignedName, assignedAge, assignedGender, assignedId,\
                    assignedPw, assignedPhoneNumber, assignedEmail))
        elif self.userTypeEntry.cget('text') == '보호자':
            userlist.append(Parent(assignedName, assignedAge, assignedGender, assignedId,\
                    assignedPw, assignedPhoneNumber, assignedEmail))
        elif self.userTypeEntry.cget('text') == '의사':
            userlist.append(Docter(assignedName, assignedAge, assignedGender, assignedId,\
                    assignedPw, assignedPhoneNumber, assignedEmail))

        userlistFile = open(file = '..//Datas//userlist.bin', mode = 'wb')
        pk.dump(userlist, file = userlistFile)
        userlistFile.close()


    def __init__(self, window: Frame) -> None:
        ############################### 로그인/회원가입 화면 ############################################
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        self.titleLabel = Label(window, text = '회원가입', bg = '#09FFFA', font = ('Arial', 50, 'bold'))
        self.titleLabel.place(x = 250, y = 100)

        self.nameLabel = Label(window, text = '이름', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.ageLabel = Label(window, text = '나이', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.genderLabel = Label(window, text = '성별', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.idLabel = Label(window, text = 'ID', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.pwLabel = Label(window, text = 'PW', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.phoneNumberLabel = Label(window, text = '연락처', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.emailLabel = Label(window, text = '이메일', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.userTypeLabel = Label(window, text = '사용자 종류', bg = '#09FFFA', font = ('Arial', 15, 'bold'))

        self.nameEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.ageEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.genderEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.idEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.pwEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.phoneNumberEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.emailEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))
        self.userTypeEntry = Entry(window, width = 25, font = ('Arial', 15, 'bold'))

        self.nameLabel.place(x = 200, y = 250); self.nameEntry.place(x = 275, y = 250)
        self.ageLabel.place(x = 200, y = 300); self.ageEntry.place(x = 275, y = 300)
        self.genderLabel.place(x = 200, y = 350); self.genderEntry.place(x = 275, y = 350)
        self.idLabel.place(x = 200, y = 400); self.idEntry.place(x = 275, y = 400)
        self.pwLabel.place(x = 200, y = 450); self.pwEntry.place(x = 275, y = 450)
        self.phoneNumberLabel.place(x = 200, y = 500); self.phoneNumberEntry.place(x = 275, y = 500)
        self.emailLabel.place(x = 200, y = 550); self.emailEntry.place(x = 275, y = 550)
        self.userTypeLabel.place(x = 200, y = 600); self.userTypeEntry.place(x = 275, y = 600)

        self.registerButton = Button(window, text = '가입', font = ('Arial', 15, 'bold'),\
                command = self.assignUser)
        self.registerButton.place(x = 350, y = 650)