from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import pickle as pk
from login_frame import LoginFrame
from assign_frame import AssignFrame
from user import User

from add_content import AddContent
from view_content import ViewContent
from add_request import AddRequest # [추가]
from view_request import ViewRequest # [추가]

class MainFrame(Frame, User):

    def openMainFrame(self) -> None:
        mainFrame = Tk()
        mainFrame.geometry('800x800')

        loginFrame = LoginFrame()
        assignFrame = AssignFrame()

        mainFrame.mainloop()

    def open_add_content_window(self):
        # 의사용: 콘텐츠 추가 창
        new_window = Toplevel(self)
        new_window.title("콘텐츠 추가")
        new_window.geometry("800x800")
        
        frame = AddContent(new_window)
        frame.pack(fill="both", expand=True)

    def open_view_content_window(self):
        # 환자용: 콘텐츠 조회 창
        new_window = Toplevel(self)
        new_window.title("내 콘텐츠 확인")
        new_window.geometry("800x800")
        
        frame = ViewContent(new_window, self.user.getId())
        frame.pack(fill="both", expand=True)

    # [추가] 환자용: 요청 보내기 창 열기
    def open_request_change_window(self):
        new_window = Toplevel(self)
        new_window.title("변경 요청 보내기")
        new_window.geometry("400x500")
        frame = AddRequest(new_window, self.user.getId())
        frame.pack(fill="both", expand=True)

    # [추가] 의사용: 요청 모아보기 창 열기
    def open_view_requests_window(self):
        new_window = Toplevel(self)
        new_window.title("변경 요청함")
        new_window.geometry("500x600")
        frame = ViewRequest(new_window)
        frame.pack(fill="both", expand=True)

    def __init__(self, window: Frame, user: User) -> None:
        super().__init__(window, bg = "#09FFC6", width = 800, height = 800)

        self.user = user

        self.mainTitleLabel = Label(window, text = '메인 메뉴', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.mainTitleLabel.place(x = 300, y = 50)


        self.menuLabel_1 = Label(window, text = '건강 데이터', font = ('Arial', 10, 'bold'), bg = "#E6FF09")
        self.menuLabel_1.place(x = 160, y = 140)

        self.F1A1_Button = Button(window, text = '건강 데이터 입력', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A1_Button.place(x = 150, y = 180)

        self.F1A2_Button = Button(window, text = '건강 데이터 조회', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A2_Button.place(x = 150, y = 210)

        self.F1B_Button = Button(window, text = '위험도 조회', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1B_Button.place(x = 150, y = 240)

        self.F1C1_Button = Button(window, text = '개인 리포트', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1C1_Button.place(x = 150, y = 270)

        self.F1C2_Button = Button(window, text = '알림 설정', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1C2_Button.place(x = 150, y = 300)

        self.F1A3_Button = Button(window, text = '식단 기록', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A3_Button.place(x = 150, y = 330)

        self.F1A4_Button = Button(window, text = '식단 추천', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A4_Button.place(x = 150, y = 360)


        self.menuLabel_2 = Label(window, text = '콘텐츠', font = ('Arial', 10, 'bold'), bg = "#E6FF09")
        self.menuLabel_2.place(x = 320, y = 140)

        self.F2A_Button = Button(window, text = '친구 관리', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F2A_Button.place(x = 300, y = 180)

        self.F2B_Button = Button(window, text = '배지 개수 확인', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F2B_Button.place(x = 300, y = 210)

        self.F3B_Button = Button(window, text = '콘텐츠 확인', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3B_Button.place(x = 300, y = 240)
        self.F3B_Button.config(command = self.open_view_content_window)


        self.F3A_Button = Button(window, text = '콘텐츠 관리', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3A_Button.place(x = 300, y = 270)
        self.F3A_Button.config(command = self.open_add_content_window)
        

        self.F3D2_Button = Button(window, text = '콘텐츠 변경 요청', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3D2_Button.place(x = 300, y = 300)
        self.F3D2_Button.config(command = self.open_request_change_window)

        self.F3D2_1_Button = Button(window, text = '변경 요청 확인', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3D2_1_Button.place(x = 300, y = 330)
        self.F3D2_1_Button.config(command = self.open_view_requests_window)

        self.menuLabel_3 = Label(window, text = '환자 관리', font = ('Arial', 10, 'bold'), bg = "#E6FF09")
        self.menuLabel_3.place(x = 470, y = 140)

        self.F4A_Button = Button(window, text = '환자 패널 보기', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F4A_Button.place(x = 460, y = 180)


        self.menuLabel_4 = Label(window, text = '개인정보 관리', font = ('Arial', 10, 'bold'), bg = "#E6FF09")
        self.menuLabel_4.place(x = 610, y = 140)

        self.F5P_Button = Button(window, text = '비밀번호 재설정', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F5P_Button.place(x = 610, y = 180)

        self.F5C_Button = Button(window, text = '가족 공유 연결', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F5C_Button.place(x = 610, y = 210)

        self.F5D_Button = Button(window, text = '주치의 연결', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F5D_Button.place(x = 610, y = 240)

        self._config_button()

    def _config_button(self):
        user_type = self.user.getUserType()

        if user_type == 'Patient' : 
                self.F4A_Button.config(state = DISABLED)
                self.F3A_Button.config(state = DISABLED)
                self.F3D2_1_Button.config(state = DISABLED)
                
        elif user_type == 'Docter' : 
              self.F1A1_Button.config(state = DISABLED)
              self.F1A2_Button.config(state = DISABLED)
              self.F1B_Button.config(state = DISABLED)
              self.F1C1_Button.config(state = DISABLED)
              self.F1C2_Button.config(state = DISABLED)
              self.F1A3_Button.config(state = DISABLED)
              self.F1A4_Button.config(state = DISABLED)
              self.F2A_Button.config(state = DISABLED)
              self.F2B_Button.config(state = DISABLED)
              self.F3B_Button.config(state = DISABLED)
              self.F3D2_Button.config(state = DISABLED)
              self.F5C_Button.config(state = DISABLED)
        elif user_type == 'Parent' :
              self.F1A1_Button.config(state = DISABLED)
              self.F3A_Button.config(state = DISABLED)
              self.F1B_Button.config(state = DISABLED)
              self.F1C1_Button.config(state = DISABLED)
              self.F1C2_Button.config(state = DISABLED)
              self.F1A3_Button.config(state = DISABLED)
              self.F1A4_Button.config(state = DISABLED)
              self.F2A_Button.config(state = DISABLED)
              self.F2B_Button.config(state = DISABLED)
              self.F3B_Button.config(state = DISABLED)
              self.F3D2_Button.config(state = DISABLED)
              self.F4A_Button.config(state = DISABLED)
              self.F5D_Button.config(state = DISABLED)
              self.F3D2_1_Button.config(state = DISABLED)
 