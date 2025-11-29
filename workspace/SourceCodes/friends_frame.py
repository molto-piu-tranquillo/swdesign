DEBUG = True

from tkinter import *
import tkinter.messagebox
from user import Patient, Data

class FriendsFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        self.__patient = patient

        self.titleLabel = Label(window, text = '친구', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 350, y = 75)

        self.friendsLabel = None
        self.friendPanelList: list[Frame] = []
        self.showFriendList()

        self.editFriendsButton = Button(window, text = '친구 목록 수정', font = ('Arial', 15, 'bold'), bg = 'white', width = 12)
        self.competeButton = Button(window, text = '경쟁', font = ('Arial', 15, 'bold'), bg = 'yellow', width = 8)

        """
        self.testButton = Button(window, text = '친구 목록 숨김', font = ('Arial', 15, 'bold'),\
                bg = 'white', command = self.hideFriendList)
        self.testButton.place(x = 400, y = 400)
        """
        
        self.editFriendsButton.place(x = 240, y = 725); self.competeButton.place(x = 410, y = 725)

    def showFriendList(self): # 친구 목록을 보여줌.
        if len(self.__patient.getFriendList()) == 0: # 친구 목록이 없을 경우
            self.friendsLabel = Label(window, text = '아직 친구가 없네요!\n친구를 추가하고 경쟁해보세요!',\
                    font = ('Arial', 15, 'bold'), bg = '#09FFFA')
            self.friendsLabel.place(x = 250, y = 400)
        else: # 친구 목록이 있을 경우
            friendList: list[Patient] = self.__patient.getFriendList()
            for i in range(len(friendList)):
                friendFrame = Frame(window, width = 600, height = 50, bg = 'white')
                friendLabel = Label(friendFrame, text = '@{:25s} 이름: {:15s} | 성별: {} | 나이: {:6d}세'\
                        .format(friendList[i].getId(), friendList[i].getName(), friendList[i].getGender(), friendList[i].getAge()),\
                        font = ('Arial', 12, 'bold'), bg = 'white')
                friendLabel.place(x = 12, y = 12)
                self.friendPanelList.append(friendFrame)

            for i in range(len(self.friendPanelList)):
                self.friendPanelList[i].place(x = 100, y = 150 + 60 * i)

    def hideFriendList(self): # 친구 목록을 숨김.
        if self.friendsLabel != None:
            self.friendsLabel.place_forget()
        else:
            for i in range(len(self.friendPanelList)):
                self.friendPanelList[i].place_forget()
            self.friendPanelList.clear()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))
    
    friend1 = Patient('SSS', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    friend2 = Patient('가가가', 11, '남', 'uk3000', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.addFriend(friend1)
    patient.addFriend(friend2)

    frame = FriendsFrame(window, patient)
    frame.pack()

    window.mainloop()