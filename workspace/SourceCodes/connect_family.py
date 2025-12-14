# 가족 연결 관련 코드

DEBUG = False

from tkinter import *
from tkinter import messagebox
from user import User, Patient, Parent, Data
import pickle as pk
import random as rd

class ConnectParentFromPatientFrame(Frame): # 환자 입장에서 보호자 연결
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__patient = patient

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '보호자 연결', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 300, y = 75)

        self.parentIdLabel = Label(self, text = '보호자 ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.parentIdEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 38)
        self.findParentByIdButton = Button(self, text = '검색', font = ('Arial', 10, 'bold'), bg = 'yellow',\
                width = 6, command = lambda: self.findParentById())

        self.commentLabel = Label(self, text = 'ID를 검색해서 보호자를 추가해보세요!', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.parentInfoFrame = None
        self.commentLabel.place(x = 230, y = 430)

        self.parentIdLabel.place(x = 100, y = 175); self.parentIdEntry.place(x = 200, y = 175); self.findParentByIdButton.place(x = 630, y = 175)

    def findParentById(self): # ID 기준으로 보호자를 찾는 메소드
        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        if len(userlist) == 0:
            if self.parentInfoFrame != None:
                self.parentInfoFrame.place_forget()
                self.parentInfoFrame = None
            self.commentLabel.place(230, y = 430)
            self.commentLabel.config(text = '해당 아이디의 보호자가 존재하지 않습니다.')
        else:
            for i in range(len(userlist)):
                if self.parentIdEntry.get() == userlist[i].getId() and userlist[i].getUserType() == '보호자':
                    self.commentLabel.place_forget()

                    if self.parentInfoFrame == None:
                        self.parentInfoFrame = Frame(self, width = 550, height = 450, bg = 'white')

                    self.parentIconLabel = Label(self.parentInfoFrame, text = '🧑', font = ('Arial', 150, 'bold'), bg = 'white')
                    self.parentIdLabel = Label(self.parentInfoFrame, text = '@{}'.format(userlist[i].getId()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.parentNameLabel = Label(self.parentInfoFrame, text = '이름: {}'.format(userlist[i].getName()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.parentGenderLabel = Label(self.parentInfoFrame, text = '성별: {}'.format(userlist[i].getGender()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.parentAgeLabel = Label(self.parentInfoFrame, text = '나이: {}세'.format(userlist[i].getAge()), font = ('Arial', 14, 'bold'), bg = 'white')

                    self.parentIconLabel.place(x = 50, y = 30)
                    self.parentIdLabel.place(x = 300, y = 70)
                    self.parentNameLabel.place(x = 300, y = 120)
                    self.parentGenderLabel.place(x = 300, y = 170)
                    self.parentAgeLabel.place(x = 300, y = 220)

                    self.connectParentButton = Button(self.parentInfoFrame, text = '보호자 연결', font = ('Arial', 14, 'bold'),\
                            bg = 'yellow', command = lambda: self.connectParent(self.parentIdEntry.get()))
                    self.deleteParentButton = Button(self.parentInfoFrame, text = '보호자 삭제', font = ('Arial', 14, 'bold'),\
                            bg = 'red', command = lambda: self.deleteParent(self.parentIdEntry.get()))

                    self.connectParentButton.place(x = 157, y = 350); self.deleteParentButton.place(x = 283, y = 350)

                    self.parentInfoFrame.place(x = 125, y = 275)
                    break
                if i == len(userlist) - 1:
                    if self.parentInfoFrame != None:
                        self.parentInfoFrame.place_forget()
                        self.parentInfoFrame = None
                    self.commentLabel.place(x = 210, y = 430)
                    self.commentLabel.config(text = '해당 아이디의 보호자가 존재하지 않습니다.')

    def connectParent(self, parentId: str): # 보호자 연결 요청 메소드
        if self.__patient.getConnectedParentId() == self.parentIdEntry.get():
            messagebox.showinfo('알림', '이미 연결되어 있는 보호자입니다.')
            return
        elif self.__patient.getConnectedParentId() != '':
            select = messagebox.askyesno('알림', '이미 연결되어 있는 보호자를 삭제하고 새로 연결하시겠습니까?')
            if select:
                self.__patient.setConnectedParentId('')
            else:
                messagebox.showinfo('알림', '보호자 연결을 취소합니다.')
                return
        
        patientId: str = self.__patient.getId()
        inviteCode = '' # 초대 코드는 6자리로 설정
        for i in range(6):
            randCharList: list[chr] = []
            randCharList.append(chr(rd.randint(ord('A'), ord('Z'))))
            randCharList.append(chr(rd.randint(ord('a'), ord('z'))))
            randCharList.append(chr(rd.randint(ord('0'), ord('9'))))
            inviteCode += randCharList[rd.randint(0, len(randCharList) - 1)]

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break
        for i in range(len(userlist)):
            if userlist[i].getId() == self.parentIdEntry.get():
                userlist[i].setInviteCodeList(patientId, inviteCode)
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '보호자 연결을 요청하였습니다.\n초대 코드: {}'.format(inviteCode))

    def deleteParent(self, parentId: str): # 보호자 삭제 메소드
        if self.__patient.getConnectedParentId() != parentId:
            messagebox.showinfo('알림', '연결되어 있지 않는 보호자입니다.')
            return
        else:
            deletedParentId: str = self.__patient.getConnectedParentId()
            self.__patient.setConnectedParentId('')

            userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
            userlist: list[User] = pk.load(file = userlistFile)
            userlistFile.close()

            for i in range(len(userlist)):
                if userlist[i].getId() == self.__patient.getId():
                    userlist[i] = self.__patient
                    break
            for i in range(len(userlist)):
                if userlist[i].getId() == deletedParentId:
                    userlist[i].deletePatientById(self.__patient.getId())
                    break

            userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
            pk.dump(file = userlistFile, obj = userlist)
            userlistFile.close()

            messagebox.showinfo('알림', '보호자가 삭제되었습니다.')

    def closeFrame(self): # 현채 창을 닫는 메소드
        self.place_forget()

class ConnectPatientFromParentFrame(Frame): # 보호자 입장에서 환자 연결
    def __init__(self, window: Frame, parent: Parent):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__parent = parent

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '환자 연결', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 300, y = 75)

        self.patientIdLabel = Label(self, text = '환자 ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.inviteCodeLabel = Label(self, text = '초대 코드', font = ('Arial', 15, 'bold'), bg = '#09FFFA')

        self.patientIdEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 35)
        self.inviteCodeEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 35)

        self.patientIdLabel.place(x = 150, y = 300); self.patientIdEntry.place(x = 250, y = 300)
        self.inviteCodeLabel.place(x = 150, y = 450); self.inviteCodeEntry.place(x = 250, y = 450)

        self.cancelButton = Button(self, text = '취소', font = ('Arial', 14, 'bold'), bg = 'white', width = 8, command = lambda: self.closeFrame())
        self.connectPatientButton = Button(self, text = '환자 연결', font = ('Arial', 14, 'bold'), bg = 'yellow', width = 8, command = lambda: self.connectPatient())

        self.cancelButton.place(x = 270, y = 625); self.connectPatientButton.place(x = 390, y = 625)

    def connectPatient(self): # 환자를 연결하는 메소드
        if self.patientIdEntry.get() == '':
            messagebox.showerror('오류', '환자 ID가 입력되지 않았습니다.')
            return
        if self.inviteCodeEntry.get() == '':
            messagebox.showerror('오류', '초대 코드가 입력되지 않있습니다')
            return
        if self.__parent.getInviteCodeTuple()[0] != self.patientIdEntry.get() or self.__parent.getInviteCodeTuple()[1] != self.inviteCodeEntry.get():
            messagebox.showerror('오류', '입력하신 정보를 다시 확인하세요.')
            return
        for i in range(len(self.__parent.getPatientIdList())):
            if self.__parent.getPatientIdList()[i] == self.patientIdEntry.get():
                messagebox.showinfo('알림', '이미 연결된 환자입니다.')
                return

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        addedPatientId = self.__parent.getInviteCodeTuple()[0]
        self.__parent.setInviteCodeList('', '')
        self.__parent.addPatientById(addedPatientId)

        for i in range(len(userlist)):
            if userlist[i].getId() == self.patientIdEntry.get():
                userlist[i].setConnectedParentId(self.__parent.getId())
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '환자 연결이 완료되었습니다.')
        self.closeFrame()

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()



if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('정재욱', 22, '남', 'uk3181', 'uk3181@', '010-9494-5836',\
            'uk3181@daum.net', '개인 사용자')
    parent = Parent('김부모', 50, '남', 'parent123', 'parent123@', '010-1111-2222',\
            'uk3181@knu.ac.kr', '보호자')
    
    userlist: list[User] = []
    userlist.append(patient)
    userlist.append(parent)

    # frame = ConnectParentFromPatientFrame(window, patient)
    frame = ConnectPatientFromParentFrame(window, parent)
    frame.pack()

    window.mainloop()