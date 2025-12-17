# 알림 관련 코드

DEBUG = False

from tkinter import *
from tkinter import messagebox
from user import *
import pickle as pk

class NotificationFrame(Frame):
    def __init__(self, window: Frame, user: User):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__user = user

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '알림', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 350, y = 100)

        self.noNotificationLabel = Label(self, text = '알림이 없습니다.', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.notificationPanelList: list[Frame] = [] # 알림 패널 리스트
        self.showNotifiactions()

    def showNotifiactions(self): # 알림 목록을 보여주는 메소드
        for i in range(len(self.notificationPanelList)):
            self.notificationPanelList[i].place_forget()
        self.notificationPanelList.clear()

        if len(self.__user.getNotificatinoList()) == 0:
            self.noNotificationLabel.place(x = 320, y = 400)
        else:
            startIndex = 0
            if len(self.__user.getNotificatinoList()) > 10:
                startIndex += len(self.__user.getNotificatinoList()) - 10 # 12 => 2~11
            for i in range(startIndex, len(self.__user.getNotificatinoList())):
                notificationPanel = Frame(self, width = 600, height = 50, bg ='white')
                notificationLabel = Label(notificationPanel, text = self.__user.getNotificatinoList()[i],\
                        font = ('Arial', 11, 'bold'), bg = 'white')
                notificationLabel.place(x = 14, y = 14)
                deleteNotificationButton = Button(notificationPanel, text = 'X', font = ('Arial', 9, 'bold'),\
                        bg = 'red', fg = 'white', width = 2, borderwidth = 1,\
                        command = lambda notification = self.__user.getNotificatinoList()[i]: self.deleteNotification(notification))
                deleteNotificationButton.place(x = 565, y = 13)
                self.notificationPanelList.append(notificationPanel)

        for i in range(len(self.notificationPanelList)):
            self.notificationPanelList[i].place(x = 100, y = 180 + 56 * i)

    def deleteNotification(self, notification: str): # 알림 목록 하나를 없애는 메소드
        self.__user.deleteNotification(notification)

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__user.getId():
                userlist[i] = self.__user
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        self.showNotifiactions()

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data = Data(1000, 10, 10, [10, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    for i in range(12):
        notification = chr(65 + i) * 30
        patient.addNotification(notification)

    frame = NotificationFrame(window, patient)
    frame.pack()

    window.mainloop()