# 위험도 조회

DEBUG = False

from tkinter import *
from tkinter import messagebox
import pickle as pk
from user import *
from data_paths import USERLIST_PATH

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

        totalDanger: int = 0 # 전체 위험도 수치
        bloodPressureDanger: int = 0 # 혈압 위험도
        bloodSugarDanger: int = 0 # 혈당 위험도
        smokeDanger: int = 0 # 흡연 위험도
        alchoholDanger: int = 0 # 음주 위험도
        eatDanger: int = 0 # 식단 위험도
        exerciseDanger: int = 0 # 활동량 위험도

        dataList: list[Data] = self.__patient.getDataList()
        lastData: Data = dataList[len(dataList) - 1]

        # 1. 혈압 위험도 계산
        if lastData.getBloodPressure()[0] >= 140 or lastData.getBloodPressure()[1] >= 90:
            bloodPressureDanger += 2
        elif lastData.getBloodPressure()[0] >= 120 or lastData.getBloodPressure()[1] >= 80:
            bloodPressureDanger += 1
        # 2. 혈당 위험도 계산
        if lastData.getBloodSugar() >= 200:
            bloodSugarDanger += 2
        elif lastData.getBloodSugar() >= 140:
            bloodSugarDanger += 1
        # 3. 흡연/음주 위험도 계산
        if lastData.getSmoke():
            smokeDanger += 1
        if lastData.getAlchohol():
            alchoholDanger += 1
        # 4. 식단 위험도 계산
        if self.__patient.getGender() == '남':
            if lastData.getCarboKcal() + lastData.getProteinKcal() + lastData.getFatKcal() >= 2500:
                eatDanger += 1
        elif self.__patient.getGender() == '여':
            if lastData.getCarboKcal() + lastData.getProteinKcal() + lastData.getFatKcal() >= 2000:
                eatDanger += 1
        # 5. 활동량 위험도 계산
        if lastData.getExerciseKcal() < 300:
            exerciseDanger += 1

        # => 전체 위험도 계산
        totalDanger += (bloodPressureDanger + bloodSugarDanger + smokeDanger + alchoholDanger + eatDanger + exerciseDanger)

        if totalDanger >= 4:
            messagebox.showinfo('알림', '건강 위험도가 높습니다!\n')

            # 건강 위험도가 높을 경우, 환자 및 보호자에게 알림을 보냄.
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
            result: str = ''
            if value:
                result += '네'
            else:
                result += '아니오'
            return result

        self.commentLabel.place_forget()
        
        self.analysisResultPanel = Frame(self, width = 600, height = 500, bg = 'white')
        self.analysisResultPanel.place(x = 100, y = 175)

        self.analysisResultLabel = Label(self.analysisResultPanel, text = '산출 결과', font = ('Arial', 18, 'bold'), bg = 'white')
        self.analysisResultLabel.place(x = 250, y = 25)

        self.bloodPressureResultLabel = Label(self.analysisResultPanel,\
                text = '혈압(수축기/이완기): {}/{}'.format(lastData.getBloodPressure()[0], lastData.getBloodPressure()[1]),\
                font = ('Arial', 15, 'bold'), bg = 'white')
        if bloodPressureDanger > 0:
            self.bloodPressureResultLabel.config(fg = 'red', text = '⚠️ ' + self.bloodPressureResultLabel.cget('text'))
        
        self.bloodSugarResultLabel = Label(self.analysisResultPanel,\
                text = '혈당: {}mg/dL'.format(lastData.getBloodSugar()), font = ('Arial', 15, 'bold'), bg = 'white')
        if bloodSugarDanger > 0:
            self.bloodSugarResultLabel.config(fg = 'red', text = '⚠️ ' + self.bloodSugarResultLabel.cget('text'))

        self.smokeResultLabel = Label(self.analysisResultPanel,\
                text = '흡연 여부: {}'.format(boolToStr(lastData.getSmoke())), font = ('Arial', 15, 'bold'), bg = 'white')
        if smokeDanger > 0:
            self.smokeResultLabel.config(fg = 'red', text = '⚠️ ' + self.smokeResultLabel.cget('text'))

        self.alchoholResultLabel = Label(self.analysisResultPanel,\
                text = '음주 여부: {}'.format(boolToStr(lastData.getAlchohol())), font = ('Arial', 15, 'bold'), bg = 'white')
        if alchoholDanger > 0:
            self.alchoholResultLabel.config(fg = 'red', text = '⚠️ ' + self.alchoholResultLabel.cget('text'))

        self.eatResultLabel = Label(self.analysisResultPanel,\
                text = '섭취량: {}kcal'.format(lastData.getCarboKcal() + lastData.getProteinKcal() + lastData.getFatKcal()),\
                font = ('Arial', 15, 'bold'), bg = 'white')
        if eatDanger > 0:
            self.eatResultLabel.config(fg = 'red', text = '⚠️ ' + self.eatResultLabel.cget('text'))

        self.exerciseResultLabel = Label(self.analysisResultPanel,\
                text = '활동량: {}kcal'.format(lastData.getExerciseKcal()), font = ('Arial', 15, 'bold'), bg = 'white')
        if exerciseDanger > 0:
            self.exerciseResultLabel.config(fg = 'red', text = '⚠️ ' + self.exerciseResultLabel.cget('text'))

        self.totalResultLabel = Label(self.analysisResultPanel,\
                text = '위험도: ', font = ('Arial', 15, 'bold'), bg = 'white')
        if totalDanger == 0:
            self.totalResultLabel.config(text = self.totalResultLabel.cget('text') + '안전', fg = 'green')
        elif totalDanger < 4:
            self.totalResultLabel.config(text = self.totalResultLabel.cget('text') + '주의', fg = 'orange')
        else:
            self.totalResultLabel.config(text = '⚠️ ' + self.totalResultLabel.cget('text') + '위험', fg = 'red')

        self.bloodPressureResultLabel.place(x = 50, y = 100)
        self.bloodSugarResultLabel.place(x = 50, y = 150)
        self.smokeResultLabel.place(x = 50, y = 200)
        self.alchoholResultLabel.place(x = 50, y = 250)
        self.eatResultLabel.place(x = 50, y = 300)
        self.exerciseResultLabel.place(x = 50, y = 350)
        Label(self.analysisResultPanel, text = '---------------------------------------------------------------------',\
                font = ('Arial', 15, 'bold'), bg = 'white').place(x = 50, y = 400)
        self.totalResultLabel.place(x = 50, y = 450)

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