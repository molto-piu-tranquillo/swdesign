# 식단 추천

DEBUG = False

from tkinter import *
from user import *
import pickle as pk

import random as rd

class RecommendSystem: # 식단 추천 시스템
    def __init__(self, data: Data):
        self.__data = data

        # 각 리스트는 <탄수화물 보충, 단백질 보충, 지방 보충>으로 구성됨.
        self.__menuListForDiet: list[list[tuple]] = [] # 다이어트를 위한 식단 리스트
        self.__menuListForGeneral: list[list[tuple]] = [] # 일반인을 위한 식단 리스트
        self.__menuListForGaining: list[list[tuple]] = [] # 체중 증가를 위한 식단 리스트

        self.setMenuListForDiet(); self.setMenuListForGeneral(); self.setMenuListForGaining()

    def recommend(self) -> tuple: # 식단 추천 알고리즘
        eatKcal: int = self.__data.getCarboKcal() + self.__data.getProteinKcal() + self.__data.getFatKcal()
        if eatKcal > self.__data.getExerciseKcal():
            if self.__data.getCarboKcal() <= self.__data.getProteinKcal() and self.__data.getCarboKcal() <= self.__data.getFatKcal():
                return tuple(rd.sample(self.__menuListForDiet[0], 3))
            elif self.__data.getFatKcal() <= self.__data.getCarboKcal() and self.__data.getFatKcal() <= self.__data.getProteinKcal():
                return tuple(rd.sample(self.__menuListForDiet[2], 3))
            else:
                return tuple(rd.sample(self.__menuListForDiet[1], 3))
        elif eatKcal == self.__data.getExerciseKcal():
            if self.__data.getCarboKcal() <= self.__data.getProteinKcal() and self.__data.getCarboKcal() <= self.__data.getFatKcal():
                return tuple(rd.sample(self.__menuListForGeneral[0], 3))
            elif self.__data.getFatKcal() <= self.__data.getCarboKcal() and self.__data.getFatKcal() <= self.__data.getProteinKcal():
                return tuple(rd.sample(self.__menuListForGeneral[2], 3))
            else:
                return tuple(rd.sample(self.__menuListForGeneral[2], 3))
        else:
            if self.__data.getCarboKcal() <= self.__data.getProteinKcal() and self.__data.getCarboKcal() <= self.__data.getFatKcal():
                return tuple(rd.sample(self.__menuListForGaining[0], 3))
            elif self.__data.getFatKcal() <= self.__data.getCarboKcal() and self.__data.getFatKcal() <= self.__data.getProteinKcal():
                return tuple(rd.sample(self.__menuListForGaining[2], 3))
            else:
                return tuple(rd.sample(self.__menuListForGaining[2], 3))

    def setMenuListForDiet(self):
        # 1. 탄수화물 보충
        carboMenuList: list[tuple] = [\
            ('현미밥', '닭가슴살', '시금치'),\
            ('고구마', '그릭 요거트', '아몬드'),\
            ('퀴노아', '아보카도', '토마토'),\
            ('통밀 파스타', '브로콜리', '시금치'),\
            ('고구마', '그릴드 연어'),\
            ('통곡물 토스트', '아보카도', '삶은 달걀'),\
            ('현미밥', '두부', '미역국')\
        ]
        # 2. 단백질 보충
        proteinMenuList: list[tuple] = [\
            ('그릭 요거트', '견과류', '믹스 베리'),\
            ('닭가슴살', '토마토', '삶은 달걀'),\
            ('연어 스테이크', '구운 채소'),\
            ('쇠고기 우둔살', '양상추 샐러드'),\
            ('두부 스테이크', '브로콜리'),\
            ('단백질 쉐이크', '바나나 반 개'),\
            ('구운 달걀 2개', '아보카도', '방울 토마토')\
        ]
        # 3. 지방 보충
        fatMenuList: list[tuple] = [\
            ('아보카도', '달걀', '샐러드'),\
            ('연어 스테이크', '시금치 무침'),\
            ('올리브 오일을 곁들인 샐러드', '닭가슴살'),\
            ('견과류 한 줌', '그릭 요거트'),\
            ('고등어 구이', '채소 무침'),\
            ('올리브 오일에 구운 채소', '두부'),\
            ('땅콩버터 한 스푼', '통밀 토스트')\
        ]
        self.__menuListForDiet.append(carboMenuList)
        self.__menuListForDiet.append(proteinMenuList)
        self.__menuListForDiet.append(fatMenuList)

    def setMenuListForGeneral(self):
        # 1. 탄수화물 보충
        carboMenuList: list[tuple] = [\
            ('현미밥', '된장국', '두부 조림'),\
            ('고구마', '고사리 무침'),\
            ('잡곡밥', '김치찌개', '달걀 후라이'),\
            ('콩나물밥', '오이 무침', '계란찜'),\
            ('현미밥', '청국장찌개', '나물 무침'),\
            ('해물 파전', '미소 된장국'),\
            ('배추 김치', '고등어 구이', '잡곡밥')\
        ]
        # 2. 단백질 보충
        proteinMenuList: list[tuple] = [\
            ('돼지고기 목살 구이', '미역국'),\
            ('새우젓으로 간을 한 오징어볶음', '김치'),\
            ('콩나물 국밥', '달걀 후라이'),\
            ('닭가슴살 두부 조림', '콩나물 무침'),\
            ('연어 조림', '브로콜리', '고구마'),\
            ('소불고기', '배추 겉절이'),\
            ('계란찜', '된장국', '현미밥')\
        ]
        # 3. 지방 보충
        fatMenuList: list[tuple] = [\
            ('아보카도', '현미밥', '구운 닭가슴살'),\
            ('고등어 구이', '미역국', '잡곡밥'),\
            ('올리브 오일로 구운 채소', '두부 구이'),\
            ('연어 구이', '시금치 무침', '고구마'),\
            ('두부 조림', '아몬드', '채소 무침'),\
            ('아보카도', '통밀빵', '달걀 후라이'),\
            ('코코넛 오일로 볶은 채소', '달걀 후라이')\
        ]
        self.__menuListForGeneral.append(carboMenuList)
        self.__menuListForGeneral.append(proteinMenuList)
        self.__menuListForGeneral.append(fatMenuList)

    def setMenuListForGaining(self):
        # 1. 탄수화물 보충
        carboMenuList: list[tuple] = [\
            ('현미밥', '고등어 구이', '시금치 나물', '미역국'),\
            ('잡곡밥', '소불고기', '김치', '된장찌개'),\
            ('고구마', '닭가슴살', '아보카도', '청경채'),\
            ('잡곡밥', '제육볶음', '두부 조림', '계란찜'),\
            ('통밀 파스타', '그릴드 치킨', '아보카도', '토마토 샐러드'),\
            ('파스타 알 프레도', '버섯', '브로콜리'),\
            ('볼로네제 파스타 (쇠고기 미트 소스)', '샐러드')\
        ]
        # 2. 단백질 보충
        proteinMenuList: list[tuple] = [\
            ('백미밥', '닭갈비', '고사리 나물', '미역국'),\
            ('현미밥', '두부 조림', '간장게장', '콩나물 무침'),\
            ('통밀 짜장면', '돼지고기 장조림', '김치'),\
            ('통밀 파스타', '그릴드 치킨', '아루굴라 샐러드'),\
            ('그릴드 연어', '레몬 소스를 곁들인 시금치', '토마토 샐러드'),\
            ('닭가슴살 리조또', '모짜렐라 치즈', '브로콜리'),\
            ('잡곡밥', '갈비찜', '시금치 나물', '계란찜')\
        ]
        # 3. 지방 보충
        fatMenuList: list[tuple] = [\
            ('삼겹살 구이', '상추', '마늘', '고추장'),\
            ('갈비찜', '잡곡밥', '아보카도 샐러드'),\
            ('부대찌게', '소시지 구이', '달걀 후라이', '떡'),\
            ('삼치 구이', '시금치 나물', '된장찌개', '잡곡밥'),\
            ('베이컨', '아보카도 샌드위치', '달걀 구이', '토마토'),\
            ('버팔로 윙', '셀러리', '블루 치즈 드레싱'),\
            ('리브 아이 스테이크', '아스파라거스', '마늘 버터')\
        ]
        self.__menuListForGaining.append(carboMenuList)
        self.__menuListForGaining.append(proteinMenuList)
        self.__menuListForGaining.append(fatMenuList)

class RecommendMenuFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__patient = patient

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '식단 추천', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 315, y = 75)

        self.menuPanel = Frame(self, width = 600, height = 510, bg = 'white')

        myMenu: tuple = RecommendSystem(self.__patient.getDataList()[len(self.__patient.getDataList()) - 1]).recommend()

        self.breakfastMenuPanel = Frame(self.menuPanel, width = 600, height = 170, bg = '#FBFFCA')
        breakfastMenuText = '[아침]\n'
        for i in range(len(myMenu[0])):
            breakfastMenuText += myMenu[0][i]
            if i != len(myMenu[0]):
                breakfastMenuText += '\n'
        self.breakfastLabel = Label(self.breakfastMenuPanel, text = breakfastMenuText, font = ('Arial', 15, 'bold'),\
                bg = '#FBFFCA', width = 50)
        self.breakfastLabel.place(x = 0, y = 10)

        self.lunchMenuPanel = Frame(self.menuPanel, width = 600, height = 170, bg = '#DEFFCF')
        lunchMenuText = '[점심]\n'
        for i in range(len(myMenu[1])):
            lunchMenuText += myMenu[1][i]
            if i != len(myMenu[1]):
                lunchMenuText += '\n'
        self.lunchLabel = Label(self.lunchMenuPanel, text = lunchMenuText, font = ('Arial', 15, 'bold'),\
                bg = '#DEFFCF', width = 50)
        self.lunchLabel.place(x = 0, y = 10)

        self.dinnerMenuPanel = Frame(self.menuPanel, width = 600, height = 170, bg = '#F1DDFF')
        dinnerMenuText = '[저녁]\n'
        for i in range(len(myMenu[2])):
            dinnerMenuText += myMenu[2][i]
            if i != len(myMenu[2]):
                dinnerMenuText += '\n'
        self.dinnerLabel = Label(self.dinnerMenuPanel, text = dinnerMenuText, font = ('Arial', 15, 'bold'),\
                bg = '#F1DDFF', width = 50)
        self.dinnerLabel.place(x = 0, y = 10)

        self.breakfastMenuPanel.place(x = 0, y = 0); self.lunchMenuPanel.place(x = 0, y = 170); self.dinnerMenuPanel.place(x = 0, y = 340)

        self.menuPanel.place(x = 100, y = 200)

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    patient = Patient('정재욱', 22, '남', 'jaewook3181', 'asdf1234!@#$', '010-9494-5836',\
            'uk3181@daum.net', '개인 사용자')
    patient.addData(Data(2025, 12, 25, [120, 90], 120, False, False, 400, 500, 600, 300))

    userlist: list[User] = []
    userlist.append(patient)

    userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
    pk.dump(file = userlistFile, obj = userlist)
    userlistFile.close()



    window = Tk()
    window.geometry('800x800')

    recommendMenuFrame = RecommendMenuFrame(window, patient)
    recommendMenuFrame.place(x = 0, y = 0)

    window.mainloop()