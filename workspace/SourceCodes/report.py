# 개인 리포트 관련 코드

DEBUG = False

from tkinter import *
from tkinter import messagebox
import pickle as pk
from user import *

import matplotlib.pyplot as plt

class ReportFrame(Frame):
    BLOOD_PRESSURE = 0
    BLOOD_SUGAR = 1
    EAT_KCAL = 2
    EXERCISE_KCAL = 3

    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__patient = patient

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '개인 리포트', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 300, y = 100)

        self.selectedButton = self.BLOOD_PRESSURE
        
        self.bloodPressureButton = Button(self, text = '혈압', font = ('Arial', 10, 'bold'), bg = 'yellow', width = 7,\
                borderwidth = 1)
        self.bloodSugarButton = Button(self, text = '혈당', font = ('Arial', 10, 'bold'), bg = 'white', width = 7,\
                borderwidth = 1, command = lambda: self.showGraph(self.BLOOD_SUGAR))
        self.eatKcalButton = Button(self, text = '섭취량', font = ('Arial', 10, 'bold'), bg = 'white', width = 7,\
                borderwidth = 1, command = lambda: self.showGraph(self.EAT_KCAL))
        self.exerciseKcalButton = Button(self, text = '활동량', font = ('Arial', 10, 'bold'), bg = 'white', width = 7,\
                borderwidth = 1, command = lambda: self.showGraph(self.EXERCISE_KCAL))

        self.makeDataListGraph(self.BLOOD_PRESSURE)

        self.graphImage = PhotoImage(file = '..//Images//health_data_graph.png')
        self.graphLabel = Label(self, image = self.graphImage, width = 480, height = 360, bg = 'white')
        self.graphLabel.place(x = 160, y = 200)

        self.bloodPressureButton.place(x = 215, y = 570)
        self.bloodSugarButton.place(x = 315, y = 570)
        self.eatKcalButton.place(x = 415, y = 570)
        self.exerciseKcalButton.place(x = 515, y = 570)

        self.goalLabel = Label(self, text = '목표', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.goalLabel.place(x = 160, y = 625)

        self.goalText = Text(self, font = ('Arial', 12, 'normal'), width = 53, height = 3, bg = 'white')
        self.goalText.insert('1.0', self.__patient.getGoal())
        self.goalText.place(x = 160, y = 655)

        self.saveGoalButton = Button(self, text = '저장', font = ('Arial', 10, 'bold'), bg = 'pink',\
                borderwidth = 1, command = lambda: self.saveGoal())
        self.saveGoalButton.place(x = 652, y = 670)

    def saveGoal(self): # 설정한 목표 저장
        self.__patient.setGoal(self.goalText.get('1.0', END))

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '목표가 저장되었습니다.')

    def showGraph(self, dataType: int):
        if dataType != -1:
            self.bloodPressureButton.config(bg = 'white', command = lambda: self.showGraph(self.BLOOD_PRESSURE))
            self.bloodSugarButton.config(bg = 'white', command = lambda: self.showGraph(self.BLOOD_SUGAR))
            self.eatKcalButton.config(bg = 'white', command = lambda: self.showGraph(self.EAT_KCAL))
            self.exerciseKcalButton.config(bg = 'white', command = lambda: self.showGraph(self.EXERCISE_KCAL))

            if dataType == self.BLOOD_PRESSURE:
                self.bloodPressureButton.config(bg = 'yellow', command = lambda: self.showGraph(-1))
            if dataType == self.BLOOD_SUGAR:
                self.bloodSugarButton.config(bg = 'yellow', command = lambda: self.showGraph(-1))
            if dataType == self.EAT_KCAL:
                self.eatKcalButton.config(bg = 'yellow', command = lambda: self.showGraph(-1))
            if dataType == self.EXERCISE_KCAL:
                self.exerciseKcalButton.config(bg = 'yellow', command = lambda: self.showGraph(-1))

            self.makeDataListGraph(dataType)

            self.graphImage.config(file = '..//Images//health_data_graph.png')
            self.graphLabel = Label(self, image = self.graphImage, width = 480, height = 360, bg = 'white')
            self.graphLabel.place(x = 160, y = 200)

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

        plt.savefig('..//Images//health_data_graph.png', dpi = 75)
        plt.close()

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()




if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data = Data(1000, 10, 10, [20, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    patient.addData(Data(year = 2025, month = 11, day = 16, bloodPressure = [50, 30], carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    for i in range(12):
        notification = chr(65 + i) * 30
        patient.addNotification(notification)

    frame = ReportFrame(window, patient)
    frame.place(x = 0, y = 0)

    window.mainloop()