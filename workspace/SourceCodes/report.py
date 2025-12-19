# 개인 리포트 관련 코드

DEBUG = False

from tkinter import *
from tkinter import messagebox
import pickle as pk
from user import *

import matplotlib.pyplot as plt
import os
from data_paths import USERLIST_PATH


class ReportFrame(Frame):
    BLOOD_PRESSURE = 0
    BLOOD_SUGAR = 1
    EAT_KCAL = 2
    EXERCISE_KCAL = 3

    GRAPH_PATH = '../Images/health_data_graph.png'

    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, width=800, height=800, bg='#09FFFA')
        self.__patient = patient

        # 이미지 폴더 없으면 생성
        os.makedirs('../Images', exist_ok=True)

        self.closeFrameButton = Button(
            self, text='<', bg='#09FFFA',
            font=('Arial', 15, 'bold'),
            borderwidth=0, command=self.closeFrame
        )
        self.closeFrameButton.place(x=10, y=10)

        self.titleLabel = Label(
            self, text='개인 리포트',
            font=('Arial', 30, 'bold'),
            bg='#09FFFA'
        )
        self.titleLabel.place(x=300, y=100)

        self.selectedButton = self.BLOOD_PRESSURE

        self.bloodPressureButton = Button(
            self, text='혈압', font=('Arial', 10, 'bold'),
            bg='yellow', width=7, borderwidth=1,
            command=lambda: self.showGraph(self.BLOOD_PRESSURE)
        )
        self.bloodSugarButton = Button(
            self, text='혈당', font=('Arial', 10, 'bold'),
            bg='white', width=7, borderwidth=1,
            command=lambda: self.showGraph(self.BLOOD_SUGAR)
        )
        self.eatKcalButton = Button(
            self, text='섭취량', font=('Arial', 10, 'bold'),
            bg='white', width=7, borderwidth=1,
            command=lambda: self.showGraph(self.EAT_KCAL)
        )
        self.exerciseKcalButton = Button(
            self, text='활동량', font=('Arial', 10, 'bold'),
            bg='white', width=7, borderwidth=1,
            command=lambda: self.showGraph(self.EXERCISE_KCAL)
        )

        # 최초 그래프 생성
        self.makeDataListGraph(self.BLOOD_PRESSURE)

        self.graphImage = PhotoImage(file=self.GRAPH_PATH)
        self.graphLabel = Label(
            self, image=self.graphImage,
            width=480, height=360, bg='white'
        )
        self.graphLabel.place(x=160, y=200)
        self.graphLabel.image = self.graphImage  # 참조 유지

        self.bloodPressureButton.place(x=215, y=570)
        self.bloodSugarButton.place(x=315, y=570)
        self.eatKcalButton.place(x=415, y=570)
        self.exerciseKcalButton.place(x=515, y=570)

        self.goalLabel = Label(self, text='목표', font=('Arial', 15, 'bold'), bg='#09FFFA')
        self.goalLabel.place(x=160, y=625)

        self.goalText = Text(self, font=('Arial', 12), width=53, height=3, bg='white')
        self.goalText.insert('1.0', self.__patient.getGoal())
        self.goalText.place(x=160, y=655)

        self.saveGoalButton = Button(
            self, text='저장', font=('Arial', 10, 'bold'),
            bg='pink', borderwidth=1, command=self.saveGoal
        )
        self.saveGoalButton.place(x=652, y=670)

    def saveGoal(self):
        self.__patient.setGoal(self.goalText.get('1.0', END))

        with open(USERLIST_PATH, 'rb') as f:
            userlist: list[User] = pk.load(f)

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__patient.getId():
                userlist[i] = self.__patient
                break

        with open(USERLIST_PATH, 'wb') as f:
            pk.dump(userlist, f)

        messagebox.showinfo('알림', '목표가 저장되었습니다.')

    def showGraph(self, dataType: int):
        buttons = [
            self.bloodPressureButton,
            self.bloodSugarButton,
            self.eatKcalButton,
            self.exerciseKcalButton
        ]

        for btn in buttons:
            btn.config(bg='white')

        buttons[dataType].config(bg='yellow')

        self.makeDataListGraph(dataType)

        self.graphImage = PhotoImage(file=self.GRAPH_PATH)
        self.graphLabel.config(image=self.graphImage)
        self.graphLabel.image = self.graphImage  # 참조 유지

    def makeDataListGraph(self, dataType: int):
        plt.clf()  # 중요!

        dataList: list[Data] = self.__patient.getDataList()
        dataList = dataList[-10:]

        dateList = []
        healthDataList = []

        for d in dataList:
            dateList.append(f'{d.getYear()}/{d.getMonth()}\n{d.getDay()}')

            if dataType == self.BLOOD_PRESSURE:
                healthDataList.append(tuple(d.getBloodPressure()))
            elif dataType == self.BLOOD_SUGAR:
                healthDataList.append(d.getBloodSugar())
            elif dataType == self.EAT_KCAL:
                healthDataList.append(
                    d.getCarboKcal() + d.getProteinKcal() + d.getFatKcal()
                )
            elif dataType == self.EXERCISE_KCAL:
                healthDataList.append(d.getExerciseKcal())

        if not healthDataList:
            plt.text(0.5, 0.5, '데이터 없음', ha='center', va='center')
        elif dataType == self.BLOOD_PRESSURE:
            maxBP = [x[0] for x in healthDataList]
            minBP = [x[1] for x in healthDataList]
            plt.plot(dateList, maxBP, marker='o', label='systolic')
            plt.plot(dateList, minBP, marker='o', label='diastolic')
            plt.legend()
            plt.ylabel('Blood Pressure')
            plt.title('Blood Pressure')
        else:
            plt.bar(dateList, healthDataList)
            titles = ['Blood Sugar', 'Consumption', 'Work Out']
            plt.title(titles[dataType - 1])

        plt.xticks(fontsize=7)
        plt.tight_layout()
        plt.savefig(self.GRAPH_PATH, dpi=75)
        plt.close()

    def closeFrame(self):
        self.place_forget()


if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234',
                      '010-9494-5836', 'uk3181@daum.net', '개인 사용자')

    patient.addData(Data(2025, 11, 16, [120, 80], 1, True, True, 100, 200, 300, 150))
    patient.addData(Data(2025, 11, 17, [130, 85], 1, True, True, 200, 300, 400, 250))

    frame = ReportFrame(window, patient)
    frame.place(x=0, y=0)

    window.mainloop()
