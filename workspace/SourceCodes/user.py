# 이 코드에는 사용자 클래스에 대한 정보를 저장함.

import datetime as dt

class Data:
    def __init__(self, year: int = 0, month: int = 0, day: int = 0, bloodPressure: list[int] = [0, 0], bloodSugar: int = 0,\
                smoke: bool = False, alchohol: bool = False, carboKcal: int = 0, proteinKcal: int = 0,\
                fatKcal: int = 0, exerciseKcal: int = 0):
        self.__year = year
        self.__month = month
        self.__day = day

        self.__bloodPressure: list[int] = bloodPressure # <수축기, 이완기>
        self.__bloodSugar = bloodSugar
        self.__smoke = smoke
        self.__alchohol = alchohol
        self.__carboKcal = carboKcal
        self.__proteinKcal = proteinKcal
        self.__fatKcal = fatKcal
        self.__exerciseKcal = exerciseKcal

    def setYear(self, year: int) -> None:
        self.__year = year

    def getYear(self) -> int:
        return self.__year

    def setMonth(self, month: int) -> None:
        self.__month = month

    def getMonth(self) -> int:
        return self.__month

    def setDay(self, day: int) -> None:
        self.__day = day

    def getDay(self) -> int:
        return self.__day

    def setBloodPressure(self, bloodPressure: list[int]) -> None:
        self.__bloodPressure = bloodPressure

    def getBloodPressure(self) -> list[int]:
        return self.__bloodPressure

    def setBloodSugar(self, bloodSugar: int) -> None:
        self.__bloodSugar = bloodSugar

    def getBloodSugar(self) -> int:
        return self.__bloodSugar

    def setSmoke(self, smoke: bool) -> None:
        self.__smoke = smoke

    def getSmoke(self) -> bool:
        return self.__smoke

    def setAlchohol(self, alchohol: bool) -> None:
        self.__alchohol = alchohol

    def getAlchohol(self) -> bool:
        return self.__alchohol

    def setCarboKcal(self, carboKcal: int) -> None:
        self.__carboKcal = carboKcal

    def getCarboKcal(self) -> int:
        return self.__carboKcal

    def setProteinKcal(self, proteinKcal: int) -> None:
        self.__proteinKcal = proteinKcal

    def getProteinKcal(self) -> int:
        return self.__proteinKcal

    def setFatKcal(self, fatKcal: int) -> None:
        self.__fatKcal = fatKcal

    def getFatKcal(self) -> int:
        return self.__fatKcal

    def setExerciseKcal(self, exerciseKcal: int) -> None:
        self.__exerciseKcal = exerciseKcal

    def getExerciseKcal(self) -> int:
        return self.__exerciseKcal

class User:
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        self.__name = name
        self.__age = age
        self.__gender = gender # '남'/'여'
        self.__id = id = id # 아이디
        self.__pw = pw # 비번
        self.__phoneNumber = phoneNumber # 연락처
        self.__email = email # 이메일

        self.__userType = userType # 사용자 종류 (개인 사용자, 보호자, 주치의)

        self.__notificationList: list[str] = [] # 알림 목록
        self.__messageList: list[str] = [] # 메시지 목록

    def getName(self) -> str:
        return self.__name
    
    def getAge(self) -> int:
        return self.__age

    def getGender(self) -> str:
        return self.__gender

    def getId(self) -> str:
        return self.__id

    def getPw(self) -> str:
        return self.__pw

    def setPw(self, pw: str) -> None:
        self.__pw = pw

    def getPhoneNumber(self) -> str:
        return self.__phoneNumber

    def getEmail(self) -> str:
        return self.__email

    def getUserType(self) -> str:
        return self.__userType

    def getNotificatinoList(self) -> list[str]:
        return self.__notificationList

    def addNotification(self, notification: str) -> None: # 알림 추가
        self.__notificationList.append('[{}-{}-{} {}:{}] {}'\
                .format(dt.datetime.today().year, dt.datetime.today().month, dt.datetime.today().day,\
                dt.datetime.today().hour, dt.datetime.today().minute, notification))

    def deleteNotification(self, notification: str) -> None: # 알림 삭제
        for i in range(len(self.__notificationList)):
            if self.__notificationList[i] == notification:
                self.__notificationList.pop(i)
                break

    def getMessageList(self) -> list[str]:
        return self.__messageList

    def addMessage(self, message: str) -> None: # 메시지 추가
        self.__messageList.append(message)
        if len(self.__messageList) > 200:
            self.__messageList.pop(0)

class Patient(User): # 일반 사용자(환자) 클래스
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        super().__init__(name, age, gender, id, pw, phoneNumber, email, userType)

        self.__dataList: list[Data] = [] # 건강 데이터 리스트 (시계열 기록)

        self.__connectedParentId: str = '' # 보호자 아이디
        self.__mainDocterId: str = '' # 주치의 아이디
        self.__friendIdList: list[str] = [] # 친구 목록

        self.__incentiveScore = 0 # 인센티브 점수
        self.__badgeCount = 0 # 뱃지 개수

        self.__contentList: list[str] = [] # 콘텐츠 리스트
        self.__changeRequestList: list[str] = [] # 요청 리스트

        self.__goal: str = '' # 목표

        self.__nextVisitDate: list[int] = [0, 0, 0] # 다음 진료일 [년, 월, 일]

    def setNextVisitDate(self, year: int, month: int, day: int) -> None:
        self.__nextVisitDate = [year, month, day]

    def getNextVisitDate(self) -> list[int]:
        return self.__nextVisitDate

    def setConnectedParentId(self, parentId: str) -> None:
        self.__connectedParentId = parentId

    def getConnectedParentId(self) -> str:
        return self.__connectedParentId

    def setMainDoctorId(self, mainDoctorId: str) -> None:
        self.__mainDocterId = mainDoctorId

    def getMainDoctorId(self) -> str:
        return self.__mainDocterId

    def getDataList(self) -> list[Data]: # 시계열 기록의 데이터 리스트를 가져오는 메소드
        return self.__dataList

    def setFriendIdList(self, friendIdList: list[str]) -> None:
        self.__friendIdList = friendIdList

    def getFriendIdList(self) -> list[str]:
        return self.__friendIdList

    def setBadgeCount(self, badgeCount: int) -> None:
        self.__badgeCount = badgeCount

    def getBadgeCount(self) -> int:
        return self.__badgeCount

    def addData(self, data: Data) -> None: # 시계열 기록의 데이터를 추가하는 메소드
        # self.__dataList.append(data)

        if len(self.__dataList) == 0:
            self.__dataList.append(data)
        else:
            for i in range(len(self.__dataList)):
                if data.getYear() < self.__dataList[i].getYear():
                    self.__dataList.insert(i, data)
                    break
                elif data.getYear() == self.__dataList[i].getYear():
                    if data.getMonth() < self.__dataList[i].getMonth():
                        self.__dataList.insert(i, data)
                        break
                    elif data.getMonth() == self.__dataList[i].getMonth():
                        if data.getDay() < self.__dataList[i].getDay():
                            self.__dataList.insert(i, data)
                            break
                        elif data.getDay() == self.__dataList[i].getDay():
                            self.__dataList[i] = data
                            break
                if i == len(self.__dataList) - 1:
                    self.__dataList.append(data)
                    break

    def setDataList(self, dataList: list[Data]):
        self.__dataList = dataList

    def isFriendExist(self, friendId: str) -> bool: # 아이디 기준으로 친구 목록 검색
        for i in range(len(self.__friendList)):
            if self.__friendList[i].getid() == friendId:
                return True
        return False

    def addFriend(self, friendId):
        self.__friendIdList.append(friendId)

    def setIncentiveScore(self, incentiveScore: int) -> None:
        self.__incentiveScore = incentiveScore

    def getIncentiveScore(self) -> int:
        return self.__incentiveScore

    def getContentList(self) -> list[str]:
        return self.__contentList

    def addContent(self, content: str) -> None:
        self.__contentList.append(content)

    def getChangeRequestList(self) -> list[str]:
        return self.__changeRequestList

    def addChangeRequest(self, changeRequest: str) -> None:
        self.__changeRequestList.append(changeRequest)

    def resetChangeRequestList(self):
        self.__changeRequestList.clear()

    def setGoal(self, goal: str) -> None:
        self.__goal = goal

    def getGoal(self) -> str:
        return self.__goal

class Doctor(User): # 주치의 클래스
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        super().__init__(name, age, gender, id, pw, phoneNumber, email, userType)

        self.__patientIdList: list[str] = [] # 환자 아이디 목록
        self.__inviteCodeList: list[str] = [] # 초대 요청 코드 관련 리스트 (<환자 아이디, 코드>)
        self.__inviteCodeList.append(''); self.__inviteCodeList.append('')

    def getPatientIdList(self) -> list[str]:
        return self.__patientIdList

    def setInviteCodeList(self, patientId: str, inviteCode: str) -> None:
        self.__inviteCodeList[0] = patientId
        self.__inviteCodeList[1] = inviteCode

    def getInviteCodeTuple(self) -> tuple[str]:
        return tuple(self.__inviteCodeList)

    def deletePatientById(self, deletedId: str): # 특정 환자 아이디 삭제
        for i in range(len(self.__patientIdList)):
            if self.__patientIdList[i] == deletedId:
                self.__patientIdList.pop(i)
                break

    def addPatientById(self, addedId: str): # 특정 환자 아이디 추가
        self.__patientIdList.append(addedId)

class Parent(User): # 보호자 클래스
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        super().__init__(name, age, gender, id, pw, phoneNumber, email, userType)

        self.__patientIdList: list[str] = [] # 환자 아이디 목록
        self.__inviteCodeList: list[str] = [] # 초대 요청 코드 관련 리스트 (<환자 아이디, 코드>)
        self.__inviteCodeList.append(''); self.__inviteCodeList.append('')

    def getPatientIdList(self) -> list[str]:
        return self.__patientIdList

    def setInviteCodeList(self, patientId: str, inviteCode: str) -> None:
        self.__inviteCodeList[0] = patientId
        self.__inviteCodeList[1] = inviteCode

    def getInviteCodeTuple(self) -> tuple[str]:
        return tuple(self.__inviteCodeList)

    def deletePatientById(self, deletedId: str): # 특정 환자 아이디 삭제
        for i in range(len(self.__patientIdList)):
            if self.__patientIdList[i] == deletedId:
                self.__patientIdList.pop(i)
                break

    def addPatientById(self, addedId: str): # 특정 환자 아이디 추가
        self.__patientIdList.append(addedId)