# Direct message

DEBUG = False

from tkinter import *
from tkinter import messagebox
from user import *
import pickle as pk

import datetime as dt

class DirectMessageFrame(Frame):
    def __init__(self, window: Frame, user: User):
        super().__init__(window, width = 350, height = 700, bg = '#7F0E82')
        self.__user = user

        self.titleLabel = Label(self, text = 'Direct Message', font = ('Arial', 20, 'bold'), bg = '#7F0E82', fg = 'white')
        self.titleLabel.place(x = 75, y = 25)

        self.idLabel = Label(self, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#7F0E82', fg = 'white')
        self.idEntry = Entry(self, font = ('Arial', 14, 'normal'), bg = 'white', width = 23)

        self.idLabel.place(x = 25, y = 75); self.idEntry.place(x = 60, y = 75)

        self.sendText = Text(self, font = ('Arial', 14, 'normal'), bg = 'white', width = 26, height = 4)
        self.sendText.place(x = 27, y = 130)

        self.sendButton = Button(self, text = '전송', font = ('Arial', 10, 'bold'), bg = 'yellow', width = 7,\
                borderwidth = 1, command = lambda: self.sendMessage())
        self.sendButton.place(x = 140, y = 230)

        self.showedMessages = Text(self, font = ('Arial', 11, 'normal'), bg = 'white', width = 36, height = 22, state = 'disabled')
        self.showMessageList()
        self.showedMessages.place(x = 27, y = 290)

    def sendMessage(self): # 메시지를 보내는 메소드
        if self.idEntry.get() == '':
            messagebox.showerror('오류', 'ID가 입력되지 않았습니다.')
            return

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        receivedUser: User = None
        for i in range(len(userlist)):
            if userlist[i].getId() == self.idEntry.get():
                if self.sendText.get('1.0', END).strip() == '':
                    messagebox.showerror('오류', '메시지가 입력되지 않았습니다.')
                    return
                receivedUser: User = userlist[i]
                break
            if i == len(userlist) - 1:
                messagebox.showerror('오류', '존재하지 않는 ID입니다.')
                return

        sendedMessage: str = '[{}-{}-{} {}:{} (발신)] @{}\n{}'\
                .format(dt.datetime.today().year, dt.datetime.today().month, dt.datetime.today().day,\
                dt.datetime.today().hour, dt.datetime.today().minute,\
                self.idEntry.get(), self.sendText.get('1.0', END)) # 발신
        receivedMessage: str = '[{}-{}-{} {}:{} (수신)] @{}\n{}'\
                .format(dt.datetime.today().year, dt.datetime.today().month, dt.datetime.today().day,\
                dt.datetime.today().hour, dt.datetime.today().minute,\
                self.__user.getId(), self.sendText.get('1.0', END)) # 수신

        self.__user.addMessage(sendedMessage)
        if self.__user.getId() != receivedUser.getId():
            receivedUser.addMessage(receivedMessage)

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__user.getId():
                userlist[i] = self.__user
                break
        if self.__user.getId() != receivedUser.getId():
            for i in range(len(userlist)):
                if userlist[i].getId() == receivedUser.getId():
                    userlist[i] = receivedUser
                    break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '메시지 전송이 완료되었습니다.')
        self.showMessageList()

    def showMessageList(self): # 메시지 기록을 보여주는 메소드
        messageList: list[str] = self.__user.getMessageList()
        showedMessagesInfo: str = ''
        for i in range(len(messageList)):
            showedMessagesInfo += messageList[i]
            if i != len(messageList):
                showedMessagesInfo += '\n'
        self.showedMessages.config(state = 'normal')
        self.showedMessages.delete('1.0', END)
        self.showedMessages.insert('1.0', showedMessagesInfo)
        self.showedMessages.config(state = 'disabled')



if DEBUG:
    # window = Tk()
    # window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data = Data(1000, 10, 10, [10, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    userlist: list[User] = []
    userlist.append(patient)

    userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
    pk.dump(file = userlistFile, obj = userlist)
    userlistFile.close()

    dmWindow = Tk()
    dmWindow.geometry('350x700')

    frame = DirectMessageFrame(dmWindow, patient)
    frame.place(x = 0, y = 0)

    dmWindow.mainloop()

    # window.mainloop()