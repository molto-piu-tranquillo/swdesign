# 환자 관리 코드

DEBUG = False

from tkinter import *
from tkinter import messagebox
import pickle as pk
import matplotlib.pyplot as plt

from user import *
from data_paths import USERLIST_PATH

class PatientInfoPanel(Frame): # 환자 정보를 보여주는 작은 패널
    GENERAL_INFO = 0
    RISK_INFO = 1
    DATA_GRAPH_INFO = 2
    GOAL_INFO = 3

    BLOOD_PRESSURE = 10
    BLOOD_SUGAR = 11
    EAT_KCAL = 12
    EXERCISE_KCAL = 13

    def __init__(self, window: Frame, width: int, height: int, patient: Patient):
        super().__init__(window, width = width, height = height, bg = 'white')
        self.__patient = patient

        self.generalInfoLabel = Label(self, text = '기본 정보', font = ('Arial', 17, 'bold'), bg = 'white')
        self.generalInfoLabel.place(x = 250, y = 30)

        self.openedInfo = self.GENERAL_INFO

        self.idLabel = Label(self, text = 'ID: {}'.format(self.__patient.getId()), font = ('Arial', 15, 'bold'), bg = 'white')
        self.nameLabel = Label(self, text = '이름: {}'.format(self.__patient.getName()), font = ('Arial', 15, 'bold'), bg = 'white')
        self.genderLabel = Label(self, text = '성별: {}'.format(self.__patient.getGender()), font = ('Arial', 15, 'bold'), bg = 'white')
        self.ageLabel = Label(self, text = '나이: {}세'.format(self.__patient.getAge()), font = ('Arial', 15, 'bold'), bg = 'white')
        self.phoneNumberLabel = Label(self, text = '전화번호: {}'.format(self.__patient.getPhoneNumber()), font = ('Arial', 15, 'bold'), bg = 'white')
        self.emailLabel = Label(self, text = '이메일: {}'.format(self.__patient.getEmail()), font = ('Arial', 15, 'bold'), bg = 'white')

        self.idLabel.place(x = 50, y = 100)
        self.nameLabel.place(x = 50, y = 150)
        self.genderLabel.place(x = 50, y = 200)
        self.ageLabel.place(x = 50, y = 250)
        self.phoneNumberLabel.place(x = 50, y = 300)
        self.emailLabel.place(x = 50, y = 350)

        self.generalInfoButton = Button(self, text = '기본 정보', font = ('Arial', 12, 'bold'), bg = 'yellow', borderwidth = 1, width = 11)
        self.riskInfoButton = Button(self, text = '위험도 조회', font = ('Arial', 12, 'bold'), bg = 'white', borderwidth = 1,\
                width = 11, command = lambda: self.showRiskInfo())
        self.dataGraphInfoButton = Button(self, text = '건강 추이 조회', font = ('Arial', 12, 'bold'), bg = 'white', borderwidth = 1,\
                width = 11, command = lambda: self.showDataGraphInfo())
        self.goalInfoButton = Button(self, text = '목표 조회', font = ('Arial', 12, 'bold'), bg = 'white', borderwidth = 1,\
                width = 11, command = lambda: self.showGoalInfo())

        self.generalInfoButton.place(x = 30, y = 450)
        self.riskInfoButton.place(x = 170, y = 450)
        self.dataGraphInfoButton.place(x = 310, y = 450)
        self.goalInfoButton.place(x = 450, y = 450)

        self.setIncentiveButton = Button(self, text = '인센티브\n부여', font = ('Arial', 12, 'bold'), bg = '#FFD6FD',\
                borderwidth = 1, command = lambda: self.setIncentiveToPatient())
        self.setIncentiveButton.place(x = 515, y = 5)

        self.setNextVisitButton = Button(self, text = '다음\n진료일', font = ('Arial', 12, 'bold'), bg = '#D6F5FF',\
                borderwidth = 1, command = lambda: self.showSetNextVisitDialog())
        self.setNextVisitButton.place(x = 445, y = 5)

        self.analysisDanger()

    def setIncentiveToPatient(self): # 인센티브 부여 메소드
        if len(self.__patient.getDataList()) < 2:
            messagebox.showinfo('알림', '2개 이상의 건강 데이터가 입력되지 않았습니다.')
            return
        
        incentiveScore: int = 0
        dataList: list[Data] = self.__patient.getDataList()
        prevData: Data = dataList[len(dataList) - 2]; currData: Data = dataList[len(dataList) - 1]

        if (prevData.getBloodPressure()[0] >= 140 and prevData.getBloodPressure()[1] >= 90)\
                and (currData.getBloodPressure()[0] < 120 and currData.getBloodPressure()[1] < 80):
            incentiveScore += 2
        elif (prevData.getBloodPressure()[0] >= 120 and prevData.getBloodPressure()[0] < 140\
                and prevData.getBloodPressure()[1] >= 80 and prevData.getBloodPressure()[1] < 90)\
                and (currData.getBloodPressure()[0] < 120 and currData.getBloodPressure()[1] < 80):
            incentiveScore += 1

        if prevData.getBloodSugar() >= 200 and currData.getBloodSugar() < 140:
            incentiveScore += 2
        elif (prevData.getBloodSugar() >= 140 and prevData.getBloodSugar() < 200) and currData.getBloodSugar() < 140:
            incentiveScore += 1

        if (prevData.getSmoke() == True and prevData.getAlchohol() == True)\
                and (currData.getSmoke() == False and currData.getAlchohol() == False):
            incentiveScore += 2

        if currData.getExerciseKcal() >= prevData.getExerciseKcal() * 1.15:
            incentiveScore += 1

        self.__patient.setIncentiveScore(incentiveScore)
        self.__patient.addNotification('인센티브가 부여되었습니다.')

        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break

        userlistFile = open(USERLIST_PATH, mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '인센티브 부여가 완료되었습니다.')

    def showSetNextVisitDialog(self): # 다음 진료일 설정 다이얼로그
        dialog = Toplevel(self)
        dialog.title('다음 진료일 설정')
        dialog.geometry('300x150')

        Label(dialog, text = '다음 진료일 (년/월/일)', font = ('Arial', 12, 'bold')).pack(pady = 10)

        entryFrame = Frame(dialog)
        entryFrame.pack()

        yearEntry = Entry(entryFrame, width = 6, font = ('Arial', 12))
        monthEntry = Entry(entryFrame, width = 4, font = ('Arial', 12))
        dayEntry = Entry(entryFrame, width = 4, font = ('Arial', 12))

        yearEntry.pack(side = LEFT, padx = 2)
        Label(entryFrame, text = '/', font = ('Arial', 12)).pack(side = LEFT)
        monthEntry.pack(side = LEFT, padx = 2)
        Label(entryFrame, text = '/', font = ('Arial', 12)).pack(side = LEFT)
        dayEntry.pack(side = LEFT, padx = 2)

        def saveNextVisit():
            try:
                year = int(yearEntry.get())
                month = int(monthEntry.get())
                day = int(dayEntry.get())
            except:
                messagebox.showerror('오류', '올바른 날짜를 입력하세요.')
                return

            self.__patient.setNextVisitDate(year, month, day)

            userlistFile = open(USERLIST_PATH, mode = 'rb')
            userlist: list[User] = pk.load(file = userlistFile)
            userlistFile.close()

            for i in range(len(userlist)):
                if userlist[i].getId() == self.__patient.getId():
                    userlist[i] = self.__patient
                    break

            userlistFile = open(USERLIST_PATH, mode = 'wb')
            pk.dump(file = userlistFile, obj = userlist)
            userlistFile.close()

            messagebox.showinfo('알림', '다음 진료일이 설정되었습니다.\n{}/{}/{}'.format(year, month, day))
            dialog.destroy()

        Button(dialog, text = '저장', font = ('Arial', 11, 'bold'), bg = '#D6F5FF', command = saveNextVisit).pack(pady = 15)

    def analysisDanger(self): # 위험도 산출 메소드
        if len(self.__patient.getDataList()) == 0:
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

        def boolToStr(value: bool) -> str:
            result: str = ''
            if value:
                result += '네'
            else:
                result += '아니오'
            return result

        self.analysisResultLabel = Label(self, text = '위험도', font = ('Arial', 17, 'bold'), bg = 'white')

        self.bloodPressureResultLabel = Label(self,\
                text = '혈압(수축기/이완기): {}/{}'.format(lastData.getBloodPressure()[0], lastData.getBloodPressure()[1]),\
                font = ('Arial', 15, 'bold'), bg = 'white')
        if bloodPressureDanger > 0:
            self.bloodPressureResultLabel.config(fg = 'red', text = '⚠️ ' + self.bloodPressureResultLabel.cget('text'))
        
        self.bloodSugarResultLabel = Label(self,\
                text = '혈당: {}mg/dL'.format(lastData.getBloodSugar()), font = ('Arial', 15, 'bold'), bg = 'white')
        if bloodSugarDanger > 0:
            self.bloodSugarResultLabel.config(fg = 'red', text = '⚠️ ' + self.bloodSugarResultLabel.cget('text'))

        self.smokeResultLabel = Label(self,\
                text = '흡연 여부: {}'.format(boolToStr(lastData.getSmoke())), font = ('Arial', 15, 'bold'), bg = 'white')
        if smokeDanger > 0:
            self.smokeResultLabel.config(fg = 'red', text = '⚠️ ' + self.smokeResultLabel.cget('text'))

        self.alchoholResultLabel = Label(self,\
                text = '음주 여부: {}'.format(boolToStr(lastData.getAlchohol())), font = ('Arial', 15, 'bold'), bg = 'white')
        if alchoholDanger > 0:
            self.alchoholResultLabel.config(fg = 'red', text = '⚠️ ' + self.alchoholResultLabel.cget('text'))

        self.eatResultLabel = Label(self,\
                text = '섭취량: {}kcal'.format(lastData.getCarboKcal() + lastData.getProteinKcal() + lastData.getFatKcal()),\
                font = ('Arial', 15, 'bold'), bg = 'white')
        if eatDanger > 0:
            self.eatResultLabel.config(fg = 'red', text = '⚠️ ' + self.eatResultLabel.cget('text'))

        self.exerciseResultLabel = Label(self,\
                text = '활동량: {}kcal'.format(lastData.getExerciseKcal()), font = ('Arial', 15, 'bold'), bg = 'white')
        if exerciseDanger > 0:
            self.exerciseResultLabel.config(fg = 'red', text = '⚠️ ' + self.exerciseResultLabel.cget('text'))

        self.totalResultLabel = Label(self,\
                text = '위험도: ', font = ('Arial', 15, 'bold'), bg = 'white')
        if totalDanger == 0:
            self.totalResultLabel.config(text = self.totalResultLabel.cget('text') + '안전', fg = 'green')
        elif totalDanger < 4:
            self.totalResultLabel.config(text = self.totalResultLabel.cget('text') + '주의', fg = 'orange')
        else:
            self.totalResultLabel.config(text = '⚠️ ' + self.totalResultLabel.cget('text') + '위험', fg = 'red')

    def makeDataListGraph(self, dataType: int): # 건강 데이터 추이에 대한 그래프를 그리는 메소드
        dataList: list[Data] = self.__patient.getDataList()
        if len(dataList) > 10: # 최대 10개의 데이터만 보여주도록 함.
            tempDataList = []
            for i in range(len(dataList) - 10, len(dataList)):
                tempDataList.append(dataList[i])
            dataList = tempDataList

        dateList: list = []; healthDataList: list = []
        for i in range(len(dataList)):
            dateInfo = '{}/{}\n{}'.format(dataList[i].getYear(), dataList[i].getMonth(), dataList[i].getDay())
            dateList.append(dateInfo)
        for i in range(len(dataList)):
            if dataType == self.BLOOD_PRESSURE:
                healthDataList.append(tuple(dataList[i].getBloodPressure()))
            elif dataType == self.BLOOD_SUGAR:
                healthDataList.append(dataList[i].getBloodSugar())
            elif dataType == self.EAT_KCAL:
                healthDataList.append(dataList[i].getCarboKcal() + dataList[i].getProteinKcal() + dataList[i].getFatKcal())
            elif dataType == self.EXERCISE_KCAL:
                healthDataList.append(dataList[i].getExerciseKcal())

        if dataType == self.BLOOD_PRESSURE:
            maxBloodPressureList: list[int] = []; minBloodPressureList: list[int] = []
            for i in range(len(healthDataList)):
                maxBloodPressureList.append(healthDataList[i][0])
                minBloodPressureList.append(healthDataList[i][1])
            plt.plot(dateList, maxBloodPressureList, color = 'red', marker = 'o', label = 'systolic')
            plt.plot(dateList, minBloodPressureList, color = 'blue', marker = 'o', label = 'diastolic')
            plt.legend()
        else:
            plt.bar(dateList, healthDataList, color = 'orange')

        plt.xticks(fontname = 'Arial', fontsize = 7, fontweight = 'normal')
        plt.yticks(fontname = 'Arial', fontsize = 9, fontweight = 'normal')

        plt.xlabel('Date', fontname = 'Arial', fontsize = 10, fontweight = 'bold')
        if dataType == self.BLOOD_PRESSURE:
            plt.title('Blood Pressure', fontname = 'Arial', fontsize = 30, fontweight = 'bold')
            plt.ylabel('Blood Pressure', fontname = 'Arial', fontsize = 10, fontweight = 'bold')
        elif dataType == self.BLOOD_SUGAR:
            plt.title('Blood Sugar', fontname = 'Arial', fontsize = 30, fontweight = 'bold')
            plt.ylabel('mg/dL', fontname = 'Arial', fontsize = 10, fontweight = 'bold')
        elif dataType == self.EAT_KCAL:
            plt.title('Consumption', fontname = 'Arial', fontsize = 30, fontweight = 'bold')
            plt.ylabel('kcal', fontname = 'Arial', fontsize = 10, fontweight = 'bold')
        elif dataType == self.EXERCISE_KCAL:
            plt.title('Work Out', fontname = 'Arial', fontsize = 30, fontweight = 'bold')
            plt.ylabel('kcal', fontname = 'Arial', fontsize = 10, fontweight = 'bold')

        plt.savefig('..//Images//health_data_graph.png', dpi = 60)
        plt.close()

    def showBloodPressureGraph(self):
        if self.selectedGraphType == self.BLOOD_SUGAR:
            self.bloodSugarGraphButton.config(bg = 'white', command = lambda: self.showBloodSugarGraph())
        elif self.selectedGraphType == self.EAT_KCAL:
            self.eatKcalGraphButton.config(bg = 'white', command = lambda: self.showEatKcalGraph())
        elif self.selectedGraphType == self.EXERCISE_KCAL:
            self.exerciseKcalGraphButton.config(bg = 'white', command = lambda: self.showExerciseGraph())
        self.selectedGraphType = self.BLOOD_PRESSURE
        self.bloodPressureGraphButton.config(bg = 'yellow', command = lambda: None)

        self.graphImageLabel.place_forget()
        self.makeDataListGraph(self.BLOOD_PRESSURE)
        self.graphImage.config(file = '..//Images//health_data_graph.png')
        self.graphImageLabel = Label(self, image = self.graphImage, width = 384, height = 288, bg = 'black', borderwidth = 1)
        self.graphImageLabel.place(x = 108, y = 110)

    def showBloodSugarGraph(self):
        if self.selectedGraphType == self.BLOOD_PRESSURE:
            self.bloodPressureGraphButton.config(bg = 'white', command = lambda: self.showBloodPressureGraph())
        elif self.selectedGraphType == self.EAT_KCAL:
            self.eatKcalGraphButton.config(bg = 'white', command = lambda: self.showEatKcalGraph())
        elif self.selectedGraphType == self.EXERCISE_KCAL:
            self.exerciseKcalGraphButton.config(bg = 'white', command = lambda: self.showExerciseGraph())
        self.selectedGraphType = self.BLOOD_SUGAR
        self.bloodSugarGraphButton.config(bg = 'yellow', command = lambda: None)

        self.graphImageLabel.place_forget()
        self.makeDataListGraph(self.BLOOD_SUGAR)
        self.graphImage.config(file = '..//Images//health_data_graph.png')
        self.graphImageLabel = Label(self, image = self.graphImage, width = 384, height = 288, bg = 'black', borderwidth = 1)
        self.graphImageLabel.place(x = 108, y = 110)

    def showEatKcalGraph(self):
        if self.selectedGraphType == self.BLOOD_PRESSURE:
            self.bloodPressureGraphButton.config(bg = 'white', command = lambda: self.showBloodPressureGraph())
        elif self.selectedGraphType == self.BLOOD_SUGAR:
            self.bloodSugarGraphButton.config(bg = 'white', command = lambda: self.showBloodSugarGraph())
        elif self.selectedGraphType == self.EXERCISE_KCAL:
            self.exerciseKcalGraphButton.config(bg = 'white', command = lambda: self.showExerciseGraph())
        self.selectedGraphType = self.EAT_KCAL
        self.eatKcalGraphButton.config(bg = 'yellow', command = lambda: None)

        self.graphImageLabel.place_forget()
        self.makeDataListGraph(self.EAT_KCAL)
        self.graphImage.config(file = '..//Images//health_data_graph.png')
        self.graphImageLabel = Label(self, image = self.graphImage, width = 384, height = 288, bg = 'black', borderwidth = 1)
        self.graphImageLabel.place(x = 108, y = 110)

    def showExerciseGraph(self):
        if self.selectedGraphType == self.BLOOD_PRESSURE:
            self.bloodPressureGraphButton.config(bg = 'white', command = lambda: self.showBloodPressureGraph())
        elif self.selectedGraphType == self.BLOOD_SUGAR:
            self.bloodSugarGraphButton.config(bg = 'white', command = lambda: self.showBloodSugarGraph())
        elif self.selectedGraphType == self.EAT_KCAL:
            self.eatKcalGraphButton.config(bg = 'white', command = lambda: self.showEatKcalGraph())
        self.selectedGraphType = self.EXERCISE_KCAL
        self.exerciseKcalGraphButton.config(bg = 'yellow', command = lambda: None)

        self.graphImageLabel.place_forget()
        self.makeDataListGraph(self.EXERCISE_KCAL)
        self.graphImage.config(file = '..//Images//health_data_graph.png')
        self.graphImageLabel = Label(self, image = self.graphImage, width = 384, height = 288, bg = 'black', borderwidth = 1)
        self.graphImageLabel.place(x = 108, y = 110)

    def saveComment(self): # 코맨트를 저장하는 메소드
        if self.commentText.get('1.0', END).strip() == '':
            messagebox.showerror('오류', '내용이 입력되지 않았습니다.')
            return

        self.__patient.setGoal(self.__patient.getGoal() + '\n[Comment]\n' + self.commentText.get('1.0', END))
        self.__patient.addNotification('목표 설정에 대한 주치의의 의견이 추가되었습니다.')

        userlistFile = open(USERLIST_PATH, mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break
        
        userlistFile = open(USERLIST_PATH, mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '입력이 완료되었습니다.')

        self.goalText.config(state = 'normal')
        self.goalText.delete('1.0', END)
        self.goalText.insert('1.0', self.__patient.getGoal())
        self.goalText.config(state = 'disabled')

    def showGeneralInfo(self): # 기본 정보를 보여주는 메소드
        if self.openedInfo == self.RISK_INFO:
            self.hideRiskInfo()
            self.riskInfoButton.config(bg = 'white', command = lambda: self.showRiskInfo())
        elif self.openedInfo == self.DATA_GRAPH_INFO:
            self.hideDataGraphInfo()
            self.dataGraphInfoButton.config(bg = 'white', command = lambda: self.showDataGraphInfo())
        elif self.openedInfo == self.GOAL_INFO:
            self.hideGoalInfo()
            self.goalInfoButton.config(bg = 'white', command = lambda: self.showGoalInfo())
        self.openedInfo = self.GENERAL_INFO
        self.generalInfoButton.config(bg = 'yellow', command = lambda: None)

        self.generalInfoLabel.place(x = 250, y = 30)

        self.idLabel.place(x = 50, y = 100)
        self.nameLabel.place(x = 50, y = 150)
        self.genderLabel.place(x = 50, y = 200)
        self.ageLabel.place(x = 50, y = 250)
        self.phoneNumberLabel.place(x = 50, y = 300)
        self.emailLabel.place(x = 50, y = 350)

    def hideGeneralInfo(self): # 기본 정보를 숨기는 메소드
        self.generalInfoLabel.place_forget()

        self.idLabel.place_forget()
        self.nameLabel.place_forget()
        self.genderLabel.place_forget()
        self.ageLabel.place_forget()
        self.phoneNumberLabel.place_forget()
        self.emailLabel.place_forget()

    def showRiskInfo(self): # 위험도 수치를 보여주는 메소드
        if len(self.__patient.getDataList()) == 0:
            messagebox.showinfo('알림', '아직까지 입력된 건강 데이터가 없습니다.')
            return

        if self.openedInfo == self.GENERAL_INFO:
            self.hideGeneralInfo()
            self.generalInfoButton.config(bg = 'white', command = lambda: self.showGeneralInfo())
        elif self.openedInfo == self.DATA_GRAPH_INFO:
            self.hideDataGraphInfo()
            self.dataGraphInfoButton.config(bg = 'white', command = lambda: self.showDataGraphInfo())
        elif self.openedInfo == self.GOAL_INFO:
            self.hideGoalInfo()
            self.goalInfoButton.config(bg = 'white', command = lambda: self.showGoalInfo())
        self.openedInfo = self.RISK_INFO
        self.riskInfoButton.config(bg = 'yellow', command = lambda: None)

        self.analysisResultLabel.place(x = 270, y = 30)

        self.bloodPressureResultLabel.place(x = 50, y = 100)
        self.bloodSugarResultLabel.place(x = 50, y = 140)
        self.smokeResultLabel.place(x = 50, y = 180)
        self.alchoholResultLabel.place(x = 50, y = 220)
        self.eatResultLabel.place(x = 50, y = 260)
        self.exerciseResultLabel.place(x = 50, y = 300)
        self.lineLabel = Label(self, text = '---------------------------------------------------------------------',\
                font = ('Arial', 15, 'bold'), bg = 'white')
        self.lineLabel.place(x = 50, y = 340)
        self.totalResultLabel.place(x = 50, y = 380)

    def hideRiskInfo(self): # 위험도 수치를 숨기는 메소드
        self.analysisResultLabel.place_forget()

        self.bloodPressureResultLabel.place_forget()
        self.bloodSugarResultLabel.place_forget()
        self.smokeResultLabel.place_forget()
        self.alchoholResultLabel.place_forget()
        self.eatResultLabel.place_forget()
        self.exerciseResultLabel.place_forget()
        self.lineLabel.place_forget()
        self.totalResultLabel.place_forget()

    def showDataGraphInfo(self): # 건강 데이터 추이를 보여주는 메소드
        if len(self.__patient.getDataList()) == 0:
            messagebox.showinfo('알림', '아직까지 입력된 건강 데이터가 없습니다.')
            return

        if self.openedInfo == self.GENERAL_INFO:
            self.hideGeneralInfo()
            self.generalInfoButton.config(bg = 'white', command = lambda: self.showGeneralInfo())
        elif self.openedInfo == self.RISK_INFO:
            self.hideRiskInfo()
            self.riskInfoButton.config(bg = 'white', command = lambda: self.showRiskInfo())
        elif self.openedInfo == self.GOAL_INFO:
            self.hideGoalInfo()
            self.goalInfoButton.config(bg = 'white', command = lambda: self.showGoalInfo())
        self.openedInfo = self.DATA_GRAPH_INFO
        self.dataGraphInfoButton.config(bg = 'yellow', command = lambda: None)

        self.selectedGraphType = self.BLOOD_PRESSURE

        self.dataGraphInfoLabel = Label(self, text = '건강 추이', font = ('Arial', 17, 'bold'), bg = 'white')
        self.dataGraphInfoLabel.place(x = 250, y = 30)

        self.bloodPressureGraphButton = Button(self, text = '혈압', font = ('Arial', 10, 'bold'), bg = 'yellow',\
                borderwidth = 1, width = 7)
        self.bloodSugarGraphButton = Button(self, text = '혈당', font = ('Arial', 10, 'bold'), bg = 'white',\
                borderwidth = 1, width = 7, command = lambda: self.showBloodSugarGraph())
        self.eatKcalGraphButton = Button(self, text = '섭취량', font = ('Arial', 10, 'bold'), bg = 'white',\
                borderwidth = 1, width = 7, command = lambda: self.showEatKcalGraph())
        self.exerciseKcalGraphButton = Button(self, text = '활동량', font = ('Arial', 10, 'bold'), bg = 'white',\
                borderwidth = 1, width = 7, command = lambda: self.showExerciseGraph())

        self.bloodPressureGraphButton.place(x = 150, y = 75)
        self.bloodSugarGraphButton.place(x = 230, y = 75)
        self.eatKcalGraphButton.place(x = 310, y = 75)
        self.exerciseKcalGraphButton.place(x = 390, y = 75)

        self.makeDataListGraph(self.BLOOD_PRESSURE)
        self.graphImage = PhotoImage(file = '..//Images//health_data_graph.png')
        self.graphImageLabel = Label(self, image = self.graphImage, width = 384, height = 288, bg = 'black', borderwidth = 1)
        self.graphImageLabel.place(x = 108, y = 110)

    def hideDataGraphInfo(self): # 건강 데이터 추이를 숨기는 메소드
        self.dataGraphInfoLabel.place_forget()

        self.bloodPressureGraphButton.place_forget()
        self.bloodSugarGraphButton.place_forget()
        self.eatKcalGraphButton.place_forget()
        self.exerciseKcalGraphButton.place_forget()

        self.graphImageLabel.place_forget()

    def showGoalInfo(self): # 목표 정보를 보여주는 메소드
        if self.openedInfo == self.GENERAL_INFO:
            self.hideGeneralInfo()
            self.generalInfoButton.config(bg = 'white', command = lambda: self.showGeneralInfo())
        elif self.openedInfo == self.RISK_INFO:
            self.hideRiskInfo()
            self.riskInfoButton.config(bg = 'white', command = lambda: self.showRiskInfo())
        elif self.openedInfo == self.DATA_GRAPH_INFO:
            self.hideDataGraphInfo()
            self.dataGraphInfoButton.config(bg = 'white', command = lambda: self.showDataGraphInfo())
        self.openedInfo = self.GOAL_INFO
        self.goalInfoButton.config(bg = 'yellow', command = lambda: None)

        self.goalInfoLabel = Label(self, text = '목표', font = ('Arial', 17, 'bold'), bg = 'white')
        self.goalInfoLabel.place(x = 275, y = 30)

        self.goalText = Text(self, width = 50, height = 10, font = ('Arial', 12, 'normal'), bg = '#D9F0FF')
        self.goalText.insert('1.0', self.__patient.getGoal())
        self.goalText.config(state = 'disabled')
        self.goalText.place(x = 75, y = 85)

        self.commentLabel = Label(self, text = 'Comment', font = ('Arial', 13, 'bold'), bg = 'white')
        self.commentLabel.place(x = 75, y = 300)

        self.commentText = Text(self, width = 50, height = 3, font = ('Arial', 12, 'normal'), bg = '#D9F0FF')
        self.commentText.place(x = 75, y = 330)

        self.saveCommentButton = Button(self, text = '저장', font = ('Arial', 10, 'bold'), bg = 'pink', width = 6,\
                borderwidth = 1, command = lambda: self.saveComment())
        self.saveCommentButton.place(x = 270, y = 390)

    def hideGoalInfo(self): # 목표 정보를 숨기는 메소드
        self.goalInfoLabel.place_forget()
        self.goalText.place_forget()
        self.commentLabel.place_forget()
        self.commentText.place_forget()
        self.saveCommentButton.place_forget()

class PatientPanelFrame(Frame):
    def __init__(self, window: Frame, doctor: Doctor):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__doctor = doctor
        
        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '환자 관리', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 315, y = 100)

        self.noPatientsLabel = Label(self, text = '아직 환자가 없네요. 환자를 추가해보세요!',\
                font = ('Arial', 15, 'bold'), bg = '#09FFFA')

        self.showPatients()

    def showPatients(self): # 환자 목록을 보여주는 메소드
        patientIdList: list[str] = self.__doctor.getPatientIdList()
        if len(patientIdList) == 0:
            self.noPatientsLabel.place(x = 210, y = 400)
        else:
            patientList: list[Patient] = [] # 주치의가 담당하는 환자 리스트
            
            userlistFile = open(USERLIST_PATH, mode = 'rb')
            userlist: list[User] = pk.load(file = userlistFile)
            userlistFile.close()

            for i in range(len(self.__doctor.getPatientIdList())):
                for j in range(len(userlist)):
                    if self.__doctor.getPatientIdList()[i] == userlist[j].getId():
                        patientList.append(userlist[j])
                        break

            self.patientPanelList: list[PatientInfoPanel] = [] # 환자 정보 패널 리스트
            self.patientInfoIndex = 0 # 몇 번째 환자 정보를 보여줄 것인지 결정
            for i in range(len(patientList)):
                patientPanel = PatientInfoPanel(self, 600, 500, patientList[i])
                self.patientPanelList.append(patientPanel)
            self.patientPanelList[self.patientInfoIndex].place(x = 100, y = 200)

            self.prevPanelButton = Button(self, text = '<', font = ('Arial', 12, 'bold'), bg = 'white', width = 3,\
                    borderwidth = 1, command = lambda: self.showPrevPatientInfo())
            self.nextPanelButton = Button(self, text = '>', font = ('Arial', 12, 'bold'), bg = 'white', width = 3,\
                    borderwidth = 1, command = lambda: self.showNextPatientInfo())

            self.prevPanelButton.place(x = 100, y = 165); self.nextPanelButton.place(x = 661, y = 165)

    def showPrevPatientInfo(self): # 이전 환자 정보를 보여주는 메소드
        self.patientPanelList[self.patientInfoIndex].place_forget()
        self.patientInfoIndex = (self.patientInfoIndex + len(self.patientPanelList) - 1) % len(self.patientPanelList)
        self.patientPanelList[self.patientInfoIndex].showGeneralInfo()
        self.patientPanelList[self.patientInfoIndex].place(x = 100, y = 200)
    
    def showNextPatientInfo(self): # 다음 환자 정보를 보여주는 메소드
        self.patientPanelList[self.patientInfoIndex].place_forget()
        self.patientInfoIndex = (self.patientInfoIndex + 1) % len(self.patientPanelList)
        self.patientPanelList[self.patientInfoIndex].showGeneralInfo()
        self.patientPanelList[self.patientInfoIndex].place(x = 100, y = 200)

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')
    
    userlist: list[User] = []

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data = Data(1000, 10, 10, [20, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    patient.addData(Data(year = 2025, month = 11, day = 16, bloodPressure = [50, 30], carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    patient2 = Patient('SSS', 15, '남', 'uwsk3111', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data2 = Data(2000, 440, 110, [120, 90], 1, True, False, 41, 112, 13, 14)
    patient2.addData(data2)

    doctor = Doctor('김의사', 30, '남', 'kimdoc', '1234', '010-9494-5836', 'uk3181@daum.net', '주치의')

    patient.setMainDoctorId(doctor.getId())
    patient2.setMainDoctorId(doctor.getId())

    doctor.addPatientById(patient.getId())
    doctor.addPatientById(patient2.getId())

    userlist.append(patient)
    userlist.append(patient2)
    userlist.append(doctor)

    userlistFile = open(USERLIST_PATH, mode = 'wb')
    pk.dump(file = userlistFile, obj = userlist)
    userlistFile.close()

    frame = PatientPanelFrame(window, doctor)
    frame.place(x = 0, y = 0)

    window.mainloop()