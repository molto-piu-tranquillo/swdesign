# 이 코드에는 사용자 클래스에 대한 정보를 저장함.

class Data:
    def __init__(self, year: int = 0, month: int = 0, day: int = 0, bloodPressure: list[int] = [0, 0], bloodSugar: int = 0,\
                smoke: bool = False, alchohol: bool = False, carboKcal: int = 0, proteinKcal: int = 0,\
                fatKcal: int = 0, exerciseKcal: int = 0):
        self.__year = year
        self.__month = month
        self.__day = day

        self.__bloodPressure = bloodPressure
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

    def getPhoneNumber(self) -> str:
        return self.__phoneNumber

    def getEmail(self) -> str:
        return self.__email

    def getUserType(self) -> str:
        return self.__userType

class Patient(User): # 일반 사용자(환자) 클래스
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        super().__init__(name, age, gender, id, pw, phoneNumber, email, userType)

        self.__dataList: list[Data] = [] # 건강 데이터 리스트 (시계열 기록)

        self.__mainDocter: User = None # 주치의
        self.__friendList: list = [] # 친구 목록

        self.__incentiveScore = 0 # 인센티브 점수
        self.__badgeCount = 0 # 뱃지 개수

    def getDataList(self) -> list[Data]: # 시계열 기록의 데이터 리스트를 가져오는 메소드
        return self.__dataList

    def setFriendList(self, friendList: list) -> None:
        self.__friendList = friendList

    def getFriendList(self) -> list:
        return self.__friendList

    def setBadgeCount(self, badgeCount: int) -> None:
        self.__badgeCount = badgeCount

    def getBadgeCount(self) -> int:
        return self.__badgeCount

    def addData(self, data: Data) -> None: # 시계열 기록의 데이터를 추가하는 메소드
        self.__dataList.append(data)

    def addFriend(self, friend):
        self.__friendList.append(friend)

class Docter(User): # 주치의 클래스
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        super().__init__(name, age, gender, id, pw, phoneNumber, email, userType)

        self.__patienList: list[Patient] = [] # 환자 목록

class Parent(User): # 보호자 클래스
    def __init__(self, name: str, age: int, gender: str, id: str, pw: str,\
            phoneNumber: str, email: str, userType: str):
        super().__init__(name, age, gender, id, pw, phoneNumber, email, userType)