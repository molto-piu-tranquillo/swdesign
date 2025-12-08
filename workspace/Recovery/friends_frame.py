DEBUG = True

from tkinter import *
import tkinter.messagebox
from user import Patient, Data, User
import pickle as pk

class CompetitionFrame(Frame):
    def __init__(self):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)

class FriendsFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        self.__patient = patient

        self.titleLabel = Label(window, text = '친구', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 350, y = 75)

        self.friendsLabel = None
        self.friendPanelList: list[Frame] = [] # 나의 친구 목록을 보여주기 위한 패널
        self.foundUserPanel = None # 아이디 기준으로 검색한 사용자 정보를 보여주기 위한 패널
        self.showFriendList()

        self.editFriendsButton = Button(window, text = '친구 목록 수정', font = ('Arial', 15, 'bold'),\
                bg = 'white', width = 12, command = lambda: self.editFriends())
        self.competeButton = Button(window, text = '경쟁', font = ('Arial', 15, 'bold'),\
                bg = 'yellow', width = 8, command = lambda: self.compete())

        self.editFriendsButton.place(x = 240, y = 725); self.competeButton.place(x = 410, y = 725)

    def findUserById(self): # 아이디 기준으로 사용자를 찾는 메소드
        if self.foundUserPanel != None:
            self.foundUserPanel.place_forget()
            self.foundUserPanel = None

        userlistFile = open('..//Datas/userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        if (len(userlist) == 0):
            self.foundUsersLabel.place(x = 250, y = 400)
        else:
            for i in range(len(userlist)):
                if userlist[i].getUserType() == '개인 사용자' and userlist[i].getId() == self.inputIdEntry.get()\
                        and userlist[i].getId() != self.__patient.getId(): # 자기 자신을 제외하고 사용자 목록 출력
                    self.foundUsersLabel.place_forget()

                    self.foundUserPanel = Frame(window, width = 550, height = 400, bg = 'white')

                    self.userIconLabel = Label(self.foundUserPanel, text = '🧑', font = ('Arial', 150, 'bold'), bg = 'white')
                    self.foundIdLabel = Label(self.foundUserPanel, text = '@{}'.format(userlist[i].getId()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.foundNameLabel = Label(self.foundUserPanel, text = '이름: {}'.format(userlist[i].getName()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.foundGenderLabel = Label(self.foundUserPanel, text = '성별: {}'.format(userlist[i].getGender()), font = ('Arial', 14, 'bold'), bg = 'white')
                    self.foundAgeLabel = Label(self.foundUserPanel, text = '나이: {}세'.format(userlist[i].getAge()), font = ('Arial', 14, 'bold'), bg = 'white')

                    self.userIconLabel.place(x = 50, y = 30)
                    self.foundIdLabel.place(x = 300, y = 70)
                    self.foundNameLabel.place(x = 300, y = 120)
                    self.foundGenderLabel.place(x = 300, y = 170)
                    self.foundAgeLabel.place(x = 300, y = 220)

                    self.addFriendButton = Button(self.foundUserPanel, text = '친구 추가', font = ('Arial', 14, 'bold'), bg = 'yellow', command = lambda: self.addFriend())
                    self.deleteFriendButton = Button(self.foundUserPanel, text = '친구 삭제', font = ('Arial', 14, 'bold'), bg = 'red', command = lambda: self.deleteFriend())

                    self.addFriendButton.place(x = 170, y = 350); self.deleteFriendButton.place(x = 280, y = 350)

                    self.foundUserPanel.place(x = 125, y = 275)
                    break
                if i == len(userlist) - 1:
                    self.foundUsersLabel.place(x = 250, y = 400)

    def addFriend(self): # 친구 추가
        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[Patient] = pk.load(userlistFile)
        userlistFile.close()

        addedFriend = None
        for i in range(len(userlist)):
            if userlist[i].getId() == self.inputIdEntry.get():
                addedFriend = userlist[i]
                break
        for i in range(len(self.__patient.getFriendList())):
            if self.__patient.getFriendList()[i].getId() == self.inputIdEntry.get():
                tkinter.messagebox.showinfo('알림', '이미 등록된 친구입니다.')
                return
        if len(self.__patient.getFriendList()) == 10: # 친구는 10명까지만 등록 가능
            tkinter.messagebox.showwarning('경고', '친구는 최대 10명까지만 등록 가능합니다.')
            return

        self.__patient.addFriend(addedFriend)
        friendListInFriend: list[Patient] = addedFriend.getFriendList()
        friendListInFriend.append(self.__patient)
        addedFriend.setFriendList(friendListInFriend)

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        tkinter.messagebox.showinfo('알림', '친구 추가가 완료되었습니다.')

    def deleteFriend(self): # 친구 삭제
        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[Patient] = pk.load(userlistFile)
        userlistFile.close()

        friendList: list[Patient] = self.__patient.getFriendList()
        if len(friendList) == 0:
            tkinter.messagebox.showinfo('알림', '친구 목록에 존재하지 않는 사용자입니다.')
            return
        else:
            for i in range(len(friendList)):
                if friendList[i].getId() == self.inputIdEntry.get():
                    friendList.pop(i)
                    self.__patient.setFriendList(friendList)
                    break
                if i == len(friendList) - 1:
                    tkinter.messagebox.showinfo('알림', '친구 목록에 존재하지 않는 사용자입니다.')
                    return
        
        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        tkinter.messagebox.showinfo('알림', '친구 삭제가 완료되었습니다.')

    def editFriends(self): # 친구 수정
        self.hideFriendList()
        self.titleLabel.place_forget()
        self.editFriendsButton.place_forget()
        self.competeButton.place_forget()

        self.editFriendsLabel = Label(window, text = '친구 목록 수정', font = ('Arial', 20, 'bold'), bg = '#09FFFA')
        self.editFriendsLabel.place(x = 300, y = 75)

        self.inputIdLabel = Label(window, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.inputIdEntry = Entry(window, font = ('Arial', 15, 'bold'), bg = 'white', width = 42)
        self.findByIdButton = Button(window, text = '검색', font = ('Arial', 10, 'bold'), bg = 'yellow',\
                width = 6, command = lambda: self.findUserById())
        
        self.inputIdLabel.place(x = 100, y = 175); self.inputIdEntry.place(x = 150, y = 175); self.findByIdButton.place(x = 630, y = 175)
        self.foundUsersLabel = Label(window, text = '해당 ID의 사용자가 존재하지 않습니다.',\
                font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.foundUsersLabel.place(x = 250, y = 400)

        self.goPrevButton = Button(window, text = '<', font = ('Arial', 15, 'bold'), bg = '#09FFFA',\
                borderwidth = 0, command = lambda: self.hideFoundUserFrame())
        self.goPrevButton.place(x = 10, y = 10)

    def hideFoundUserFrame(self): # # 사용자 검색 페이지를 숨김.
        self.editFriendsLabel.place_forget()
        self.inputIdLabel.place_forget()
        self.inputIdEntry.place_forget()
        self.findByIdButton.place_forget()
        self.foundUsersLabel.place_forget()
        if self.foundUserPanel == None:
            self.foundUsersLabel.place_forget()
        else:
            self.foundUserPanel.place_forget()
        self.goPrevButton.place_forget()

        self.titleLabel.place(x = 350, y = 75)
        self.editFriendsButton.place(x = 240, y = 725)
        self.competeButton.place(x = 410, y = 725)
        self.showFriendList()

    def compete(self): # 경쟁
        self.hideFriendList()
        self.titleLabel.place_forget()
        self.editFriendsButton.place_forget()
        self.competeButton.place_forget()
        pass

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
    
    friend1 = Patient('SSS', 10, '남', 'abfwoifj', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    friend2 = Patient('가가가', 11, '남', 'uk3000', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.addFriend(friend1);
    patient.addFriend(friend2);

    userlist: list[User] = []
    userlist.append(patient)
    userlist.append(friend1)
    userlist.append(friend2)

    userlistFile = open('..//Datas/userlist.bin', mode = 'wb')
    pk.dump(file = userlistFile, obj = userlist)
    userlistFile.close()

    frame = FriendsFrame(window, patient)
    frame.pack()

    window.mainloop()