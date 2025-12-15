DEBUG = False

from tkinter import *
from tkinter import messagebox
from user import User, Patient, Doctor, Data
import pickle as pk
import random as rd

class ConnectPatientFromDoctorFrame(Frame): # 의사 입장에서 관리 환자 연결
    def __init__(self, window: Frame, doctor: Doctor):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__doctor: Doctor = doctor

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
        if self.__doctor.getInviteCodeTuple()[0] != self.patientIdEntry.get() or self.__doctor.getInviteCodeTuple()[1] != self.inviteCodeEntry.get():
            messagebox.showerror('오류', '입력하신 정보를 다시 확인하세요.')
            return
        for i in range(len(self.__doctor.getPatientIdList())):
            if self.__doctor.getPatientIdList()[i] == self.patientIdEntry.get():
                messagebox.showinfo('알림', '이미 연결된 환자입니다.')
                return

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        addedPatientId = self.__doctor.getInviteCodeTuple()[0]
        self.__doctor.setInviteCodeList('', '')
        self.__doctor.addPatientById(addedPatientId)

        for i in range(len(userlist)):
            if userlist[i].getId() == self.patientIdEntry.get():
                userlist[i].setMainDoctorId(self.__doctor.getId())
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '환자 연결이 완료되었습니다.')
        self.closeFrame()

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()

class ConnectDoctorFromPatientFrame(Frame): # 환자 입장에서 주치의 연결 요청
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.__patient: Patient = patient

        self.titleLabel = Label(self, text = '주치의 연결', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 300, y = 100)

        self.doctorIdLabel = Label(self, text = '주치의 ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.doctorIdEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 38)
        self.findDoctorByIdButton = Button(self, text = '검색', font = ('Arial', 10, 'bold'), bg = 'yellow',\
                width = 6, command = lambda: self.findDoctorById())

        self.commentLabel = Label(self, text = 'ID를 검색해서 주치의를 추가해보세요!', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.doctorInfoFrame = None
        self.commentLabel.place(x = 230, y = 430)

        self.doctorIdLabel.place(x = 100, y = 175); self.doctorIdEntry.place(x = 200, y = 175); self.findDoctorByIdButton.place(x = 630, y = 175)

    def findDoctorById(self): # ID 기준으로 의사를 찾는 메소드
        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        if len(userlist) == 0:
            if self.doctorInfoFrame != None:
                self.doctorInfoFrame.place_forget()
                self.doctorInfoFrame = None
            self.commentLabel.place(230, y = 430)
            self.commentLabel.config(text = '해당 아이디의 의사가 존재하지 않습니다.')
        else:
            for i in range(len(userlist)):
                if self.doctorIdEntry.get() == userlist[i].getId() and userlist[i].getUserType() == '주치의':
                    self.commentLabel.place_forget()


                    if self.doctorInfoFrame == None:
                        self.doctorInfoFrame = Frame(self, width = 550, height = 450, bg = 'white')

                    self.doctorIconLabel = Label(self.doctorInfoFrame, text = '⚕️', font = ('Arial', 150, 'bold'), bg = 'white')
                    self.doctorIdLabel = Label(self.doctorInfoFrame, text = '@{}'.format(userlist[i].getId()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.doctorNameLabel = Label(self.doctorInfoFrame, text = '이름: {}'.format(userlist[i].getName()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.doctorGenderLabel = Label(self.doctorInfoFrame, text = '성별: {}'.format(userlist[i].getGender()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.doctorAgeLabel = Label(self.doctorInfoFrame, text = '나이: {}세'.format(userlist[i].getAge()), font = ('Arial', 14, 'bold'), bg = 'white')

                    self.doctorIconLabel.place(x = 30, y = 50)
                    self.doctorIdLabel.place(x = 300, y = 70)
                    self.doctorNameLabel.place(x = 300, y = 120)
                    self.doctorGenderLabel.place(x = 300, y = 170)
                    self.doctorAgeLabel.place(x = 300, y = 220)

                    self.connectDoctorButton = Button(self.doctorInfoFrame, text = '의사 연결', font = ('Arial', 14, 'bold'),\
                            bg = 'yellow', command = lambda: self.connectDoctor(self.doctorIdEntry.get()))
                    self.deleteDoctorButton = Button(self.doctorInfoFrame, text = '의사 삭제', font = ('Arial', 14, 'bold'),\
                            bg = 'red', command = lambda: self.deleteDoctor(self.doctorIdEntry.get()))

                    self.connectDoctorButton.place(x = 170, y = 350); self.deleteDoctorButton.place(x = 280, y = 350)

                    self.doctorInfoFrame.place(x = 125, y = 275)
                    break
                if i == len(userlist) - 1:
                    if self.doctorInfoFrame != None:
                        self.doctorInfoFrame.place_forget()
                        self.doctorInfoFrame = None
                    self.commentLabel.place(x = 230, y = 430)
                    self.commentLabel.config(text = '해당 아이디의 의사가 존재하지 않습니다.')

    def connectDoctor(self, doctorId: str): # 주치의 연결 요청 메소드

        if self.__patient.getMainDoctorId() == self.doctorIdEntry.get():
            messagebox.showinfo('알림', '이미 연결되어 있는 주치의입니다.')
            return
        elif self.__patient.getMainDoctorId() != '':
            select = messagebox.askyesno('알림', '이미 연결되어 있는 주치의를 삭제하고 새로 연결하시겠습니까?')
            if select:
                self.__patient.setMainDoctorId('')
            else:
                messagebox.showinfo('알림', '주치의 연결을 취소합니다.')
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
            if userlist[i].getId() == self.doctorIdEntry.get():
                userlist[i].setInviteCodeList(patientId, inviteCode)
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '주치의 연결을 요청하였습니다.\n초대 코드: {}'.format(inviteCode))

    def deleteDoctor(self, doctorId: str): # 주치의 삭제 메소드
        if self.__patient.getMainDoctorId() != doctorId:
            messagebox.showinfo('알림', '연결되어 있지 않는 주치의입니다.')
            return
        else:
            deletedDoctorId: str = self.__patient.getMainDoctorId()
            self.__patient.setMainDoctorId('')

            userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
            userlist: list[User] = pk.load(file = userlistFile)
            userlistFile.close()

            for i in range(len(userlist)):
                if userlist[i].getId() == self.__patient.getId():
                    userlist[i] = self.__patient
                    break
            for i in range(len(userlist)):
                if userlist[i].getId() == deletedDoctorId:
                    userlist[i].deletePatientById(self.__patient.getId())
                    break

            userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
            pk.dump(file = userlistFile, obj = userlist)
            userlistFile.close()

            messagebox.showinfo('알림', '주치의가 삭제되었습니다.')

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.setMainDoctorId('doc123')
    data = Data(1000, 10, 10, [10, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    frame = ConnectDoctorFromPatientFrame(window, patient)
    frame.place(x = 0, y = 0)

    window.mainloop()