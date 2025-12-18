# 뱃지 개수 확인

DEBUG = False

from tkinter import *
from user import Patient

class CheckBadgeCountFrame(Frame):
    def __init__(self, window: Frame, patient: Patient):
        super().__init__(window, width = 800, height = 800, bg = '#09FFFA')
        self.__patient = patient

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 17, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '뱃지 개수 확인', font = ('Arial', 30, 'bold'), background = '#09FFFA')
        self.titleLabel.place(x = 280, y = 75)

        self.badgeCountLabel = Label(self, text = '현재 뱃지 개수는 {}개입니다.'.format(self.__patient.getBadgeCount()),\
                font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        if self.__patient.getBadgeCount() == 0:
            self.badgeCountLabel.place(x = 280, y = 400)
        else:
            self.badgeIconLabel = Label(self, text = '🥇', font = ('Arial', 200, 'bold'), bg = '#09FFFA')
            self.badgeIconLabel.place(x = 255, y = 240)
            self.badgeCountLabel.place(x = 280, y = 575)

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()



if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    patient.setBadgeCount(1)
    patient.setMainDoctorId('doc123')

    frame = CheckBadgeCountFrame(window, patient)
    frame.place(x = 0, y = 0)

    window.mainloop()