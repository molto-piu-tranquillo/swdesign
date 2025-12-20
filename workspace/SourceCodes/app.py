DEBUG = False

from tkinter import *
from user import User
from login_frame import LoginFrame

import os

class App(Frame):
    def __init__(self, window: Frame):
        super().__init__(window, bg = "#09FFFA", width = 800, height = 800)

        self.loginFrame = LoginFrame(self)
        self.loginFrame.place(x = 0, y = 0)



# 최종 프로그램 실행 코드
def main():
    if not DEBUG:
        os.system('pip show matplotlib || pip install matplotlib') # matplotlib 모듈이 설치되어 있지 않은 경우에만 해당 모듈 설치

    window = Tk()
    window.geometry('800x800')

    appFrame: Frame = App(window)
    appFrame.place(x = 0, y = 0)

    window.mainloop()
main()