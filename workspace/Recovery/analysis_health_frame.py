DEBUG = True

from tkinter import *
from tkinter import messagebox
from user import User, Patient, Data
import pickle as pk

class AnalysisFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)
        self.__patient = patient

        self.selectLabel = Label(window, text = '다음 중 선택하세요.', font = ('Arial', 30, 'bold'),\
                background = '#09FFFA')
        self.selectLabel.place(x = 225, y = 200)

        self.selectButton1 = Button(window, text = '데이터 입력', font = ('Arial', 35, 'bold'),\
                background = 'white', command = lambda: self.inputDatas(window))
        self.selectButton2 = Button(window, text = '데이터 조회', font = ('Arial', 35, 'bold'),\
                background = 'white', command = lambda: self.checkDatas(window))

        self.selectButton1.place(x = 250, y = 400)
        self.selectButton2.place(x = 250, y = 550)

    def unpackElements(self): # 각종 레이블 버튼 숨기기
        self.selectLabel.place_forget()
        self.selectButton1.place_forget()
        self.selectButton2.place_forget()

    def repackElements(self): # 각종 레이블, 버튼 다시 보이게 하기
        self.selectLabel.place(x = 225, y = 200)
        self.selectButton1.place(x = 250, y = 400)
        self.selectButton2.place(x = 250, y = 550)

    def checkDatas(self, window: Frame): # 입력된 데이터를 확인하는 메소드
        self.unpackElements()

        dataList: list[Data] = self.__patient.getDataList()
        lastDataIndex = len(dataList) - 1

        def setButtons():
            if lastDataIndex < len(dataList) - 1:
                self.nextButton.place(x = 700, y = 200)
            if lastDataIndex > 0:
                self.prevButton.place(x = 100, y = 200)

        self.prevButton = Button(window, text = '이전', font = ('Arial', 13, 'bold'), background = 'white')
        self.nextButton = Button(window, text = '다음', font = ('Arial', 13, 'bold'), background = 'white')
        # setButtons()
        self.prevButton.place(x = 100, y = 150); self.nextButton.place(x = 700, y = 150)
        
        self.dateLabel = Label(window, text = '{}/{}/{}'.format(dataList[lastDataIndex].getYear(), dataList[lastDataIndex].getMonth(), dataList[lastDataIndex].getDay()),\
                font = ('Arial', 25, 'bold'), background = '#09FFFA')
        self.dateLabel.place(x = 330, y = 150)

        def boolToStr(value: bool) -> str: # True이면 '네', False이면 '아니오'
            if value:
                return '네'
            else:
                return '아니오'
        self.bloodPressureInfoLabel = Label(window, text = '혈압: {}/{}mmHg'.format(dataList[lastDataIndex].getBloodPressure()[0], dataList[lastDataIndex].getBloodPressure()[1]),\
                font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.bloodSugarInfoLabel = Label(window, text = '혈당: {}mg/dL'.format(dataList[lastDataIndex].getBloodSugar()),\
                font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.smokeInfoLabel = Label(window, text = '흡연 여부: {}'.format(boolToStr(dataList[lastDataIndex].getSmoke())),\
                font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.alchoholInfoLabel = Label(window, text = '음주 여부: {}'.format(boolToStr(dataList[lastDataIndex].getAlchohol())),\
                font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.carboKcalInfoLabel = Label(window, text = '● 탄수화물: {}kcal'.format(dataList[lastDataIndex].getCarboKcal()),\
                font = ('Arial', 10, 'bold'), background = '#09FFFA')
        self.proteinKcalInfoLabel = Label(window, text = '● 단백질: {}kcal'.format(dataList[lastDataIndex].getProteinKcal()),\
                font = ('Arial', 10, 'bold'), background = '#09FFFA')
        self.fatKcalInfoLabel = Label(window, text = '● 지방: {}kcal'.format(dataList[lastDataIndex].getFatKcal()),\
                font = ('Arial', 10, 'bold'), background = '#09FFFA')
        self.eatKcalLabel = Label(window,\
                text = '하루 총 섭취량: {}kcal'.format(dataList[lastDataIndex].getCarboKcal() + dataList[lastDataIndex].getProteinKcal() + dataList[lastDataIndex].getFatKcal()),\
                font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.exerciseKcalInfoLabel = Label(window, text = '활동량: {}kcal'.format(dataList[lastDataIndex].getExerciseKcal()),\
                font = ('Arial', 15, 'bold'), background = '#09FFFA')

        self.bloodPressureInfoLabel.place(x = 125, y = 250)
        self.bloodSugarInfoLabel.place(x = 125, y = 300)
        self.smokeInfoLabel.place(x = 125, y = 350)
        self.alchoholInfoLabel.place(x = 125, y = 400)
        self.eatKcalLabel.place(x = 125, y = 450)
        self.carboKcalInfoLabel.place(x = 125, y = 475)
        self.proteinKcalInfoLabel.place(x = 125, y = 495)
        self.fatKcalInfoLabel.place(x = 125, y = 515)
        self.exerciseKcalInfoLabel.place(x = 125, y = 565)

        def calcDanger(): # 위험도를 계산하는 메소드
            danger: int = 0

    def saveDatas(self): # 입력된 데이터를 저장하는 메소드
        if self.yearEntry.get() == '' or self.monthEntry.get() == '' or self.dayEntry.get() == '':
            messagebox.showerror('오류', '날짜 정보가 입력되지 않았습니다.')
            return
        else:
            try:
                savedYear = int(self.yearEntry.get())
                savedMonth = int(self.monthEntry.get())
                savedDay = int(self.dayEntry.get())
            except ValueError:
                messagebox.showerror('오류', '날짜 정보는 정수로 입력하세요.')
                return
        
        if self.bloodPressureEntry.get() == '':
            messagebox.showerror('오류', '혈압이 입력되지 않았습니다.')
            return
        else:
            if self.bloodPressureEntry.get().count('/') != 1:
                messagebox.showerror('오류', '입력 형식이 올바르지 않습니다.\n형식: 수축기/이완기')
                return
            else:
                highBloodPressure, lowBloodPressure = self.bloodPressureEntry.get().split('/')
                try:
                    highBloodPressure = int(highBloodPressure)
                    lowBloodPressure = int(lowBloodPressure)
                except ValueError:
                    messagebox.showerror('오류', '혈압은 정수로 입력하세요.')
                    return
        if self.bloodPressureEntry.get() == '':
            messagebox.showerror('오류', '혈당이 입력되지 않았습니다.')
            return
        else:
            try:
                savedBloodSugar = int(self.bloodSugarEntry.get())
            except ValueError:
                messagebox.showerror('오류', '혈당은 정수로 입력하세요.')
                return

        if self.smokeEntry.get() == '':
            messagebox.showerror('오류', '흡연 여부가 입력되지 않았습니다.')
            return
        else:
            if self.smokeEntry.get() == '네':
                savedSmoke = True
            elif self.smokeEntry.get() == '아니오':
                savedSmoke = False
            else:
                messagebox.showerror('오류', '네 또는 아니오로 입력하세요.')
                return
        if self.alchoholEntry.get() == '':
            messagebox.showerror('오류', '음주 여부가 입력되지 않았습니다')
            return
        else:
            if self.alchoholEntry.get() == '네':
                savedAlchohol = True
            elif self.alchoholEntry.get() == '아니오':
                savedAlchohol = False
            else:
                messagebox.showerror('오류', '네 또는 아니오로 입력하세요')
                return
        
        if self.carboKcalEntry.get() == '':
            messagebox.showerror('오류', '탄수화물 섭취량이 입력되지 않았습니다.')
            return
        else:
            try:
                savedCarboKcal = int(self.carboKcalEntry.get())
            except ValueError:
                messagebox.showerror('오류', '탄수화물 섭취량은 정수로 입력하세요.')
                return
        if self.proteinKcalEntry.get() == '':
            messagebox.showerror('오류', '단백질 섭취량이 입력되지 않았습니다.')
            return
        else:
            try:
                savedProteinKcal = int(self.proteinKcalEntry.get())
            except ValueError:
                messagebox.showerror('오류', '단백질 섭취량은 정수로 입력하세요.')
                return
        if self.fatKcalEntry.get() == '':
            messagebox.showerror('오류', '지방 섭취량이 입력되지 않았습니다.')
            return
        else:
            try:
                savedFatKcal = int(self.fatKcalEntry.get())
            except ValueError:
                messagebox.showerror('오류', '지방 섭취량은 정수로 입력하세요.')
                return
        
        if self.exerciseKcalEntry.get() == '':
            messagebox.showerror('오류', '활동량이 입력되지 않았습니다.')
            return
        else:
            try:
                savedExerciseKcal = int(self.exerciseKcalEntry.get())
            except ValueError:
                messagebox.showerror('오류', '활동량은 정수로 입력하세요.')
                return

        savedData = Data(savedYear, savedMonth, savedDay, [highBloodPressure, lowBloodPressure], savedBloodSugar, savedSmoke, savedAlchohol,\
                savedCarboKcal, savedProteinKcal, savedFatKcal, savedExerciseKcal)
        self.__patient.addData(savedData)

        # 데이터가 입력되면 userlist.bin 파일을 변경해야 함.
        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if self.__patient.getName() == userlist[i].getName():
                userlist[i] = self.__patient
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(userlist, file = userlistFile)
        userlistFile.close()

        # 정보 저장이 끝나면, 다시 "데이터 입력", "데이터 조회" 중 선택할 수 있도록 화면을 구성해야 함.
        self.yearLabel.place_forget(); self.yearEntry.place_forget()
        self.monthLabel.place_forget(); self.monthEntry.place_forget()
        self.dayLabel.place_forget(); self.dayEntry.place_forget()
        
        self.bloodPressureLabel.place_forget(); self.bloodPressureEntry.place_forget()
        self.bloodSugarLabel.place_forget(); self.bloodSugarEntry.place_forget()
        self.smokeLabel.place_forget(); self.smokeEntry.place_forget()
        self.alchoholLabel.place_forget(); self.alchoholEntry.place_forget()
        self.eatKcalLabel.place_forget()
        self.carboKcalLabel.place_forget(); self.carboKcalEntry.place_forget()
        self.proteinKcalLabel.place_forget(); self.proteinKcalEntry.place_forget()
        self.fatKcalLabel.place_forget(); self.fatKcalEntry.place_forget()
        self.exerciseKcalLabel.place_forget(); self.exerciseKcalEntry.place_forget()

        self.inputDatasLabel.place_forget()
        self.saveDataButton.place_forget()

        self.repackElements()
        ###############################################################################################

    def inputDatas(self, window):
        self.unpackElements()
        
        self.yearLabel = Label(window, text = '년도', font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.monthLabel = Label(window, text = '월', font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.dayLabel = Label(window, text = '일', font = ('Arial', 15, 'bold'), background = '#09FFFA')

        self.yearEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 5)
        self.monthEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 5)
        self.dayEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 5)

        self.yearLabel.place(x = 200, y = 230); self.yearEntry.place(x = 250, y = 230)
        self.monthLabel.place(x = 350, y = 230); self.monthEntry.place(x = 400, y = 230)
        self.dayLabel.place(x = 500, y = 230); self.dayEntry.place(x = 550, y = 230)

        self.bloodPressureLabel = Label(window, text = '혈압\n(수축기/이완기)', font = ('Arial', 13, 'bold'), background = '#09FFFA')
        self.bloodSugarLabel = Label(window, text = '혈당', font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.smokeLabel = Label(window, text = '흡연\n(네/아니오)', font = ('Arial', 13, 'bold'), background = '#09FFFA')
        self.alchoholLabel = Label(window, text = '음주\n(네/아니오)', font = ('Arial', 13, 'bold'), background = '#09FFFA')
        self.eatKcalLabel = Label(window, text = '하루 섭취량', font = ('Arial', 15, 'bold'), background = '#09FFFA')
        self.carboKcalLabel = Label(window, text = '탄수화물(kcal)', font = ('Arial', 12, 'bold'), background = '#09FFFA')
        self.proteinKcalLabel = Label(window, text = '단백질(kcal)', font = ('Arial', 12, 'bold'), background = '#09FFFA')
        self.fatKcalLabel = Label(window, text = '지방(kcal)', font = ('Arial', 12, 'bold'), background = '#09FFFA')
        self.exerciseKcalLabel = Label(window, text = '활동량(kcal)', font = ('Arial', 13, 'bold'), background = '#09FFFA')

        self.inputDatasLabel = Label(window, text = '건강 데이터를 입력하세요.', font = ('Arial', 25, 'bold'), background = '#09FFFA')
        self.inputDatasLabel.place(x = 200, y = 100)

        self.bloodPressureEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 30)
        self.bloodSugarEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 30)
        self.smokeEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 30)
        self.alchoholEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 30)
        self.carboKcalEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 9)
        self.proteinKcalEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 9)
        self.fatKcalEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 9)
        self.exerciseKcalEntry = Entry(window, font = ('Arial', 15, 'bold'), width = 30)

        self.bloodPressureLabel.place(x = 160, y = 290); self.bloodPressureEntry.place(x = 300, y = 300)
        self.bloodSugarLabel.place(x = 200, y = 350); self.bloodSugarEntry.place(x = 300, y = 350)
        self.smokeLabel.place(x = 180, y = 390); self.smokeEntry.place(x = 300, y = 400)
        self.alchoholLabel.place(x = 180, y = 440); self.alchoholEntry.place(x = 300, y = 450)
        self.eatKcalLabel.place(x = 170, y = 525)
        self.carboKcalLabel.place(x = 300, y = 515); self.carboKcalEntry.place(x = 300, y = 545)
        self.proteinKcalLabel.place(x = 415, y = 515); self.proteinKcalEntry.place(x = 415, y = 545)
        self.fatKcalLabel.place(x = 530, y = 515); self.fatKcalEntry.place(x = 530, y = 545)
        self.exerciseKcalLabel.place(x = 175, y = 600); self.exerciseKcalEntry.place(x = 300, y = 600)

        self.saveDataButton = Button(window, text = '저장', font = ('Arial', 15, 'bold'),\
                background = 'yellow', width = 8, command = lambda: self.saveDatas())
        self.saveDataButton.place(x = 350, y = 700)

if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    frame = AnalysisFrame(window, patient)
    frame.pack()

    window.mainloop()