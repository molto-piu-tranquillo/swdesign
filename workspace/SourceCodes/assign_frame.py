DEBUG = False

from tkinter import *
from tkinter import messagebox
import pickle as pk

from user import *

class AssignFrame(Frame):
    def assignUser(self) -> None:
        userlistFile = open(file = '..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        if self.nameEntry.get() == '':
            messagebox.showerror('오류', '이름이 입력되지 않았습니다.')
            return
        else:
            if len(self.nameEntry.get()) > 4:
                messagebox.showerror('오류', '이름은 4자 이내로 입력하세요.')
                return
            else:
                assignedName = self.nameEntry.get()
        if self.ageEntry.get() == '':
            messagebox.showerror('오류', '나이가 입력되지 않았습니다.')
            return
        else:
            try:
                assignedAge = int(self.ageEntry.get())
                if assignedAge <= 0 or assignedAge > 150:
                    messagebox.showerror('오류', '입력하신 나이를 다시 확인하세요.')
                    return
            except ValueError:
                messagebox.showerror('오류', '나이는 정수로 입력하세요.')
                return
        
        if self.genderEntry.get() == '':
            messagebox.showerror('오류', '성별을 입력하세요.')
            return
        else:
            if self.genderEntry.get() != '남' and self.genderEntry.get() != '여':
                messagebox.showerror('오류', '남 또는 여로 입력하세요.')
                return
            else:
                assignedGender = self.genderEntry.get()

        if self.idEntry.get() == '':
            memoryview.showerror('오류', '아이디가 입력되지 않았습니다.')
            return
        else:
            if len(self.idEntry.get()) < 3 or len(self.idEntry.get()) > 12:
                messagebox.showerror('오류', '아이디의 길이는 3~12자로 입력하세요.')
                return
            else:
                assignedId = self.idEntry.get()

        if self.pwEntry.get() == '':
            messagebox.showerror('오류', '비밀번호가 입력되지 않았습니다.')
            return
        else:
            if len(self.pwEntry.get()) < 3 or len(self.pwEntry.get()) > 12:
                messagebox.showerror('오류', '비밀번호의 길이는 3~12자로 입력하세요.')
                return
            else:
                assignedPw = self.pwEntry.get()

        if self.phoneNumberEntry.get() == '':
            messagebox.showerror('오류', '전화번호가 입력되지 않았습니다.')
            return
        else:
            assignedPhoneNumber = self.phoneNumberEntry.get()
            if len(assignedPhoneNumber) == 13:
                # 0 1 2 3 4 5 6 7 8 9 10 11 12
                # 0 1 0 - 9 4 9 4 - 5 8  3  6
                for i in range(len(assignedPhoneNumber)):
                    if i == 3 or i == 8:
                        if assignedPhoneNumber[i] != '-':
                            messagebox.showerror('오류', '입력하신 전화번호를 다시 확인하세요\n형식: XXX-XXXX-XXXX')
                            return
                    else:
                        if assignedPhoneNumber[i] < '0' or assignedPhoneNumber[i] > '9':
                            messagebox.showerror('오류', '입력하신 전화번호를 다시 확인하세요\n형식: XXX-XXXX-XXXX')
                            return
                pass
            else:
                messagebox.showerror('오류', '입력하신 전화번호를 다시 확인하세요\n형식: XXX-XXXX-XXXX')
                return
        if self.emailEntry.get() == '':
            messagebox.showerror('오류', '이메일이 입력되지 않았습니다.')
            return
        else:
            assignedEmail = self.emailEntry.get()
            if assignedEmail.count('@') != 1:
                messagebox.showerror('오류', '입력하신 이메일을 다시 확인하세요.')
                return
            else:
                specialCharExist = False # '@' 문자가 나왔는지 체크
                prevStrLen = 0; afterStrLen = 0 # '@' 앞뒤로 문자열의 길이를 체크함.
                for i in range(len(assignedEmail)):
                    if assignedEmail[i] == '@':
                        specialCharExist = True
                    else:
                        if specialCharExist:
                            afterStrLen += 1
                        else:
                            prevStrLen += 1
                if prevStrLen == 0 or afterStrLen == 0:
                    messagebox.showerror('오류', '입력하신 이메일을 다시 확인하세요.')
                    return

        if self.userTypeEntry.get() == '':
            messagebox.showerror('오류', '사용자 종류가 입력되지 않았습니다.')
            return
        elif self.userTypeEntry.get() == '개인 사용자':
            userlist.append(Patient(assignedName, assignedAge, assignedGender, assignedId,\
                    assignedPw, assignedPhoneNumber, assignedEmail, '개인 사용자'))
        elif self.userTypeEntry.get() == '보호자':
            userlist.append(Parent(assignedName, assignedAge, assignedGender, assignedId,\
                    assignedPw, assignedPhoneNumber, assignedEmail, '보호자'))
        elif self.userTypeEntry.get() == '의사':
            userlist.append(Doctor(assignedName, assignedAge, assignedGender, assignedId,\
                    assignedPw, assignedPhoneNumber, assignedEmail, '의사'))
        else:
            messagebox.showerror('오류', '개인 사용자, 보호자, 의사 중 입력하세요.')
            return

        userlistFile = open(file = '..//Datas//userlist.bin', mode = 'wb')
        pk.dump(userlist, file = userlistFile)
        userlistFile.close()

        messagebox.showinfo('알림', '회원가입이 완료되었습니다.')
        self.closeFrame()


    def __init__(self, window: Frame) -> None:
        ############################### 로그인/회원가입 화면 ############################################
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '회원가입', bg = '#09FFFA', font = ('Arial', 30, 'bold'))
        self.titleLabel.place(x = 300, y = 100)

        self.nameLabel = Label(self, text = '이름', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.ageLabel = Label(self, text = '나이', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.genderLabel = Label(self, text = '성별', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.idLabel = Label(self, text = 'ID', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.pwLabel = Label(self, text = 'PW', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.phoneNumberLabel = Label(self, text = '연락처', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.emailLabel = Label(self, text = '이메일', bg = '#09FFFA', font = ('Arial', 15, 'bold'))
        self.userTypeLabel = Label(self, text = '사용자\n종류', bg = '#09FFFA', font = ('Arial', 13, 'bold'))

        self.nameEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.ageEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.genderEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.idEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.pwEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.phoneNumberEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.emailEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))
        self.userTypeEntry = Entry(self, width = 25, font = ('Arial', 15, 'bold'))

        self.nameLabel.place(x = 200, y = 230); self.nameEntry.place(x = 275, y = 230)
        self.ageLabel.place(x = 200, y = 280); self.ageEntry.place(x = 275, y = 280)
        self.genderLabel.place(x = 200, y = 330); self.genderEntry.place(x = 275, y = 330)
        self.idLabel.place(x = 200, y = 380); self.idEntry.place(x = 275, y = 380)
        self.pwLabel.place(x = 200, y = 430); self.pwEntry.place(x = 275, y = 430)
        self.phoneNumberLabel.place(x = 200, y = 480); self.phoneNumberEntry.place(x = 275, y = 480)
        self.emailLabel.place(x = 200, y = 530); self.emailEntry.place(x = 275, y = 530)
        self.userTypeLabel.place(x = 200, y = 574); self.userTypeEntry.place(x = 275, y = 580)

        self.registerButton = Button(self, text = '가입', font = ('Arial', 14, 'bold'),\
                bg = 'yellow', width = 8, command = lambda: self.assignUser())
        self.cancelButton = Button(self, text = '취소', font = ('Arial', 14, 'bold'),\
                bg = 'white', width = 8, command = lambda: self.closeFrame())

        self.cancelButton.place(x = 286, y = 650); self.registerButton.place(x = 398, y = 650)

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    frame = AssignFrame(window)
    frame.pack()

    window.mainloop()