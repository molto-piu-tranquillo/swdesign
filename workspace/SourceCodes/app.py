from tkinter import *
from user import User
from login_frame import LoginFrame

class App(Frame):
    def __init__(self, window: Frame):
        super().__init__(window, bg = "#09FFFA", width = 800, height = 800)

        self.loginFrame = LoginFrame(self)
        self.loginFrame.place(x = 0, y = 0)



# 최종 프로그램 실행 코드
def main():
    window = Tk()
    window.geometry('800x800')

    appFrame: Frame = App(window)
    appFrame.place(x = 0, y = 0)

    window.mainloop()
main()