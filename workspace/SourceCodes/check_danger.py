# 위험도 조회

DEBUG = False

from tkinter import *
from tkinter import messagebox
import pickle as pk
from math import exp
from user import *
from data_paths import USERLIST_PATH


def calculateRiskProbability(age: int, hypertension: int, heartDisease: int,
                              avgGlucoseLevel: float, bmi: float) -> float:
    """로지스틱 모델을 사용한 위험도 확률 계산"""
    z = (0.03 * age
         + 0.9 * hypertension
         + 1.1 * heartDisease
         + 0.012 * avgGlucoseLevel
         + 0.05 * bmi
         - 7.0)
    prob = 1.0 / (1.0 + exp(-z))
    return max(0.0, min(1.0, prob))

class CheckDangerFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__patient = patient

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '위험도 조회', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 290, y = 75)

        self.commentLabel = Label(self, text = '아래 버튼을 눌러 위험도 산출을 시작해보세요!', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.commentLabel.place(x = 220, y = 300)

        self.analysisDangerButton = Button(self, text = '위험도 산출', font = ('Arial', 30, 'bold'), bg = 'white', command = lambda: self.analysisDanger())
        self.analysisDangerButton.place(x = 280, y = 400)

    def analysisDanger(self): # 위험도 산출 메소드
        if len(self.__patient.getDataList()) == 0:
            messagebox.showinfo('알림', '아직까지 입력된 건강 데이터가 없습니다.')
            return

        dataList: list[Data] = self.__patient.getDataList()
        lastData: Data = dataList[len(dataList) - 1]

        # 로지스틱 모델 입력값 준비
        age: int = self.__patient.getAge()
        hypertension: int = 1 if (lastData.getBloodPressure()[0] >= 140 or lastData.getBloodPressure()[1] >= 90) else 0
        heartDisease: int = 1 if lastData.getHeartDisease() else 0
        avgGlucoseLevel: float = float(lastData.getBloodSugar())
        bmi: float = lastData.getBMI()

        # 로지스틱 모델로 위험도 확률 계산
        riskProb: float = calculateRiskProbability(age, hypertension, heartDisease, avgGlucoseLevel, bmi)
        riskScore: int = round(riskProb * 10)  # 0~10 스케일

        self.__patient.setRiskScore(riskScore)
        self.__patient.addNotification('위험도가 산출되었습니다.')

        # 위험도 높음 (확률 >= 0.5, 점수 >= 5)
        if riskProb >= 0.5:
            messagebox.showinfo('알림', '건강 위험도가 높습니다!\n')

            userlistFile = open(USERLIST_PATH, mode = 'rb')
            userlist: list[User] = pk.load(file = userlistFile)
            userlistFile.close()

            self.__patient.addNotification('[위험] 건강 위험도가 높습니다! 건강 관리에 유의하세요.')
            for i in range(len(userlist)):
                if userlist[i].getId() == self.__patient.getConnectedParentId():
                    userlist[i].addNotification('[위험] {}(@{})님의 건강 위험도가 높습니다!'\
                            .format(self.__patient.getName(), self.__patient.getId()))
                    break

            userlistFile = open(USERLIST_PATH, mode = 'wb')
            pk.dump(file = userlistFile, obj = userlist)
            userlistFile.close()

        def boolToStr(value: bool) -> str:
            return '네' if value else '아니오'

        self.commentLabel.place_forget()

        self.analysisResultPanel = Frame(self, width = 600, height = 500, bg = 'white')
        self.analysisResultPanel.place(x = 100, y = 175)

        self.analysisResultLabel = Label(self.analysisResultPanel, text = '산출 결과', font = ('Arial', 18, 'bold'), bg = 'white')
        self.analysisResultLabel.place(x = 250, y = 15)

        # 기본 건강 지표
        self.bloodPressureResultLabel = Label(self.analysisResultPanel,\
                text = '혈압(수축기/이완기): {}/{}'.format(lastData.getBloodPressure()[0], lastData.getBloodPressure()[1]),\
                font = ('Arial', 13, 'bold'), bg = 'white')
        if hypertension:
            self.bloodPressureResultLabel.config(fg = 'red', text = '⚠️ ' + self.bloodPressureResultLabel.cget('text'))

        self.bloodSugarResultLabel = Label(self.analysisResultPanel,\
                text = '혈당: {}mg/dL'.format(lastData.getBloodSugar()), font = ('Arial', 13, 'bold'), bg = 'white')
        if avgGlucoseLevel >= 140:
            self.bloodSugarResultLabel.config(fg = 'red', text = '⚠️ ' + self.bloodSugarResultLabel.cget('text'))

        self.smokeResultLabel = Label(self.analysisResultPanel,\
                text = '흡연 여부: {}'.format(boolToStr(lastData.getSmoke())), font = ('Arial', 13, 'bold'), bg = 'white')
        if lastData.getSmoke():
            self.smokeResultLabel.config(fg = 'red', text = '⚠️ ' + self.smokeResultLabel.cget('text'))

        self.alchoholResultLabel = Label(self.analysisResultPanel,\
                text = '음주 여부: {}'.format(boolToStr(lastData.getAlchohol())), font = ('Arial', 13, 'bold'), bg = 'white')
        if lastData.getAlchohol():
            self.alchoholResultLabel.config(fg = 'red', text = '⚠️ ' + self.alchoholResultLabel.cget('text'))

        totalKcal = lastData.getCarboKcal() + lastData.getProteinKcal() + lastData.getFatKcal()
        kcalLimit = 2500 if self.__patient.getGender() == '남' else 2000
        self.eatResultLabel = Label(self.analysisResultPanel,\
                text = '섭취량: {}kcal'.format(totalKcal), font = ('Arial', 13, 'bold'), bg = 'white')
        if totalKcal >= kcalLimit:
            self.eatResultLabel.config(fg = 'red', text = '⚠️ ' + self.eatResultLabel.cget('text'))

        self.exerciseResultLabel = Label(self.analysisResultPanel,\
                text = '활동량: {}kcal'.format(lastData.getExerciseKcal()), font = ('Arial', 13, 'bold'), bg = 'white')
        if lastData.getExerciseKcal() < 300:
            self.exerciseResultLabel.config(fg = 'red', text = '⚠️ ' + self.exerciseResultLabel.cget('text'))

        # 로지스틱 모델 지표
        self.heartDiseaseResultLabel = Label(self.analysisResultPanel,\
                text = '심장질환: {}'.format(boolToStr(lastData.getHeartDisease())), font = ('Arial', 13, 'bold'), bg = 'white')
        if heartDisease:
            self.heartDiseaseResultLabel.config(fg = 'red', text = '⚠️ ' + self.heartDiseaseResultLabel.cget('text'))

        self.bmiResultLabel = Label(self.analysisResultPanel,\
                text = 'BMI: {:.1f} (키: {}cm, 체중: {}kg)'.format(bmi, lastData.getHeight(), lastData.getWeight()),\
                font = ('Arial', 13, 'bold'), bg = 'white')
        if bmi >= 25:
            self.bmiResultLabel.config(fg = 'red', text = '⚠️ ' + self.bmiResultLabel.cget('text'))

        # 위험도 결과
        self.totalResultLabel = Label(self.analysisResultPanel,\
                text = '위험도: ', font = ('Arial', 15, 'bold'), bg = 'white')
        if riskProb < 0.3:
            self.totalResultLabel.config(text = self.totalResultLabel.cget('text') + '안전 ({:.1%})'.format(riskProb), fg = 'green')
        elif riskProb < 0.5:
            self.totalResultLabel.config(text = self.totalResultLabel.cget('text') + '주의 ({:.1%})'.format(riskProb), fg = 'orange')
        else:
            self.totalResultLabel.config(text = '⚠️ ' + self.totalResultLabel.cget('text') + '위험 ({:.1%})'.format(riskProb), fg = 'red')

        self.bloodPressureResultLabel.place(x = 50, y = 60)
        self.bloodSugarResultLabel.place(x = 50, y = 95)
        self.smokeResultLabel.place(x = 50, y = 130)
        self.alchoholResultLabel.place(x = 50, y = 165)
        self.eatResultLabel.place(x = 50, y = 200)
        self.exerciseResultLabel.place(x = 50, y = 235)
        self.heartDiseaseResultLabel.place(x = 50, y = 270)
        self.bmiResultLabel.place(x = 50, y = 305)
        Label(self.analysisResultPanel, text = '─' * 40,\
                font = ('Arial', 12, 'bold'), bg = 'white').place(x = 50, y = 345)
        self.totalResultLabel.place(x = 50, y = 380)

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data = Data(1000, 10, 10, [10, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    # patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    frame = CheckDangerFrame(window, patient)
    frame.place(x = 0, y = 0)

    window.mainloop()
