DEBUG = False

from tkinter import *
import tkinter.messagebox
from user import Patient, Data, User
import pickle as pk
from data_paths import USERLIST_PATH

class CompetitionSys:
    def __init__(self, groupUserList: list[Patient]):
        self.__groupUserList: list[Patient] = groupUserList # 친구 관계에 속한 그룹의 사용자 리스트

    def getGroupUserList(self) -> list[Patient]:
        return self.__groupUserList

    def giveBedge(self):
        # 1. 인센티브 점수 오름차순 정렬
        incentiveScoreList = []
        for i in range(len(self.__groupUserList)):
            incentiveScoreList.append(self.__groupUserList[i].getIncentiveScore())
        incentiveScoreList.sort(reverse = True) # 오름차순 정렬

        # 2. 가장 높은 인센티브 점수를 부여한 사용자에게 뱃지 부여
        if incentiveScoreList[0] > 0: # 최고 인센티브 점수는 0점보다 커야 함.
            for i in range(len(self.__groupUserList)):
                if self.__groupUserList[i].getIncentiveScore() == incentiveScoreList[0]: # 동점자에게는 모두 뱃지 부여
                    self.__groupUserList[i].setBadgeCount(1)
                else:
                    self.__groupUserList[i].setBadgeCount(0)
        else: # 그렇지 않을 경우, 그룹 사용자 전원 뱃지 개수를 0으로 설정
            for i in range(len(self.__groupUserList)):
                self.__groupUserList[i].setBadgeCount(0)

class CompetitionFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)

        self.goPrevButton = Button(self, text = '<', font = ('Arial', 15, 'bold'), bg = '#09FFFA', borderwidth = 0)
        self.goPrevButton.place(x = 10, y = 10)

        self.groupUserPanelList: list[Frame] = [] # 인센티브 점수, 뱃지 부여 여부를 보여주는 프레임 리스트

        self.setElements(patient)

    def setElements(self, patient: Patient): # 레이블, 버튼 등 각종 요소를 보여주는 메소드
        self.__patient = patient

        self.titleLabel = Label(self, text = '경쟁', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 350, y = 75)

        self.runCompetition()

        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()
        
        groupUserList: list[Patient] = []
        groupUserList.append(self.__patient)
        for i in range(len(self.__patient.getFriendIdList())):
            for j in range(len(userlist)):
                if self.__patient.getFriendIdList()[i] == userlist[j].getId():
                    groupUserList.append(userlist[j])
                    break

        if DEBUG: # 뱃지 표시를 위한 테스트 블럭
            groupUserList[0].setBadgeCount(1)

        # 그룹 사용자를 화면에 보여주고, 뱃지가 있으면 함께 표시하기
        for i in range(len(groupUserList)):
            groupUserFrame = Frame(self, width = 600, height = 50, bg = 'white')
            groupUserLabel = Label(groupUserFrame, text = '@{:25s} 이름: {:15s} | 인센티브: {:4d}점'\
                    .format(groupUserList[i].getId(), groupUserList[i].getName(), groupUserList[i].getIncentiveScore()),\
                    font = ('Arial', 12, 'bold'), bg = 'white')
            if groupUserList[i].getBadgeCount() == 1:
                badgeLabel = Label(groupUserFrame, text = '🥇', font = ('Arial', 20, 'bold'), bg = 'white')
                badgeLabel.place(x = 550, y = 6)
            groupUserLabel.place(x = 12, y = 12)
            self.groupUserPanelList.append(groupUserFrame)

        for i in range(len(self.groupUserPanelList)):
            self.groupUserPanelList[i].place(x = 100, y = 150 + 60 * i)

    def runCompetition(self): # 경쟁 시스템 작동
        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        groupUserList: list[Patient] = []
        groupUserList.append(self.__patient)
        for i in range(len(self.__patient.getFriendIdList())):
            for j in range(len(userlist)):
                if self.__patient.getFriendIdList()[i] == userlist[j].getId():
                    groupUserList.append(userlist[j])
                    break

        competitionSys = CompetitionSys(groupUserList)
        competitionSys.giveBedge()
        groupUserList = competitionSys.getGroupUserList()

        for i in range(len(groupUserList)):
            for j in range(len(userlist)):
                if groupUserList[i].getId() == userlist[j].getId():
                    userlist[j] = groupUserList[i]
                    break

        userlistFile = open(USERLIST_PATH, mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

class FriendsFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        self.__patient: Patient = patient

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '친구', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 350, y = 75)

        self.friendsLabel = None
        self.friendPanelList: list[Frame] = [] # 나의 친구 목록을 보여주기 위한 패널
        self.foundUserPanel = None # 아이디 기준으로 검색한 사용자 정보를 보여주기 위한 패널
        self.showFriendList()

        self.editFriendsButton = Button(self, text = '친구 목록 수정', font = ('Arial', 15, 'bold'),\
                bg = 'white', width = 12, command = lambda: self.editFriends())
        self.competeButton = Button(self, text = '경쟁', font = ('Arial', 15, 'bold'),\
                bg = 'yellow', width = 8, command = lambda: self.compete(window))

        self.editFriendsButton.place(x = 240, y = 725); self.competeButton.place(x = 410, y = 725)

    def findUserById(self): # 아이디 기준으로 사용자를 찾는 메소드
        if self.foundUserPanel != None:
            self.foundUserPanel.place_forget()
            self.foundUserPanel = None

        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        if (len(userlist) == 0):
            self.foundUsersLabel.place(x = 250, y = 400)
        else:
            for i in range(len(userlist)):
                if userlist[i].getUserType() == '개인 사용자' and userlist[i].getId() == self.inputIdEntry.get()\
                        and userlist[i].getId() != self.__patient.getId(): # 자기 자신을 제외하고 사용자 목록 출력
                    self.foundUsersLabel.place_forget()

                    self.foundUserPanel = Frame(self, width = 550, height = 400, bg = 'white')

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
        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        addedFriendId = ''
        for i in range(len(userlist)):
            if userlist[i].getId() == self.inputIdEntry.get():
                addedFriendId = userlist[i].getId()
                break
        for i in range(len(self.__patient.getFriendIdList())):
            if self.__patient.getFriendIdList()[i] == self.inputIdEntry.get():
                tkinter.messagebox.showinfo('알림', '이미 등록된 친구입니다.')
                return
        if len(self.__patient.getFriendIdList()) == 10: # 친구는 10명까지만 등록 가능
            tkinter.messagebox.showwarning('경고', '친구는 최대 10명까지만 등록 가능합니다.')
            return

        self.__patient.addFriend(addedFriendId)
        addedFriend = None
        for i in range(len(userlist)):
            if userlist[i].getId() == addedFriendId:
                addedFriend = userlist[i]
                break
        addedFriend.addFriend(self.__patient.getId())

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break
        for i in range(len(userlist)):
            if userlist[i].getId() == addedFriendId:
                userlist[i] = addedFriend
                break

        userlistFile = open(USERLIST_PATH, mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        tkinter.messagebox.showinfo('알림', '친구 추가가 완료되었습니다.')

    def deleteFriend(self): # 친구 삭제
        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        friendIdList: list[Patient] = self.__patient.getFriendIdList()
        if len(friendIdList) == 0:
            tkinter.messagebox.showinfo('알림', '친구 목록에 존재하지 않는 사용자입니다.')
            return
        else:
            deletedFriend: Patient = None
            for i in range(len(friendIdList)):
                if friendIdList[i] == self.inputIdEntry.get():
                    for j in range(len(userlist)):
                        if userlist[j].getId() == friendIdList[i]:
                            deletedFriend = userlist[j]
                            break
                    break
                if i == len(friendIdList) - 1:
                    tkinter.messagebox.showinfo('알림', '친구 목록에 존재하지 않는 사용자입니다.')
                    return
        
        for i in range(len(friendIdList)):
            if friendIdList[i] == deletedFriend.getId():
                friendIdList.pop(i)
                break
        friendIdListInDeletedFriend: list[str] = deletedFriend.getFriendIdList()
        for i in range(len(friendIdListInDeletedFriend)):
            if friendIdListInDeletedFriend[i] == self.__patient.getId():
                friendIdListInDeletedFriend.pop(i)
                break

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break
        for i in range(len(userlist)):
            if userlist[i].getId() == deletedFriend.getId():
                userlist[i] = deletedFriend
                break

        userlistFile = open(USERLIST_PATH, mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        tkinter.messagebox.showinfo('알림', '친구 삭제가 완료되었습니다.')

    def editFriends(self): # 친구 수정
        self.hideFriendList()
        self.titleLabel.place_forget()
        self.editFriendsButton.place_forget()
        self.competeButton.place_forget()

        self.editFriendsLabel = Label(self, text = '친구 목록 수정', font = ('Arial', 20, 'bold'), bg = '#09FFFA')
        self.editFriendsLabel.place(x = 300, y = 75)

        self.inputIdLabel = Label(self, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.inputIdEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 42)
        self.findByIdButton = Button(self, text = '검색', font = ('Arial', 10, 'bold'), bg = 'yellow',\
                width = 6, command = lambda: self.findUserById())
        
        self.inputIdLabel.place(x = 100, y = 175); self.inputIdEntry.place(x = 150, y = 175); self.findByIdButton.place(x = 630, y = 175)
        self.foundUsersLabel = Label(self, text = '해당 ID의 사용자가 존재하지 않습니다.',\
                font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.foundUsersLabel.place(x = 250, y = 400)

        self.goPrevButton = Button(self, text = '<', font = ('Arial', 15, 'bold'), bg = '#09FFFA',\
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

    def compete(self, window: Frame): # 경쟁
        self.hideFriendList()
        self.titleLabel.place_forget()
        self.editFriendsButton.place_forget()
        self.competeButton.place_forget()
        
        self.competitionFrame = CompetitionFrame(self, self.__patient)
        self.competitionFrame.goPrevButton.config(command = lambda: self.finishCompete())
        self.competitionFrame.place(x = 0, y = 0)

    def finishCompete(self): # 경쟁 시스템을 종료하고, 다시 친구 목록 화면으로 돌아감.
        self.competitionFrame.place_forget()
        self.titleLabel.place(x = 350, y = 75)
        self.editFriendsButton.place(x = 240, y = 725); self.competeButton.place(x = 410, y = 725)
        self.showFriendList()

    def showFriendList(self): # 친구 목록을 보여줌.
        if len(self.__patient.getFriendIdList()) == 0: # 친구 목록이 없을 경우
            self.friendsLabel = Label(self, text = '아직 친구가 없네요!\n친구를 추가하고 경쟁해보세요!',\
                    font = ('Arial', 15, 'bold'), bg = '#09FFFA')
            self.friendsLabel.place(x = 250, y = 400)
        else: # 친구 목록이 있을 경우
            friendIdList: list[Patient] = self.__patient.getFriendIdList()
            friendList: list[Patient] = []

            userlistFile = open(USERLIST_PATH, mode = 'rb')
            userlist: list[User] = pk.load(userlistFile)
            userlistFile.close()

            for i in range(len(friendIdList)):
                for j in range(len(userlist)):
                    if friendIdList[i] == userlist[j].getId():
                        friendList.append(userlist[j])
                        break

            for i in range(len(friendIdList)):
                friendFrame = Frame(self, width = 600, height = 50, bg = 'white')
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

    def closeFrame(self): # 현재 창 닫기
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))
    
    friend1 = Patient('SSS', 10, '남', 'abfwoifj', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    friend2 = Patient('가가가', 11, '남', 'uk3000', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.addFriend(friend1.getId()); friend1.addFriend(patient.getId())
    patient.addFriend(friend2.getId()); friend2.addFriend(patient.getId())

    userlist: list[User] = []
    userlist.append(patient)
    userlist.append(friend1)
    userlist.append(friend2)

    userlistFile = open(USERLIST_PATH, mode = 'wb')
    pk.dump(file = userlistFile, obj = userlist)
    userlistFile.close()

    frame = FriendsFrame(window, patient)
    frame.pack()

    """
    frame = CompetitionFrame(window, patient)
    frame.pack()
    """

    window.mainloop()