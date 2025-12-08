DEBUG = False
DEBUG_FOR_PASSWORD_FRAME = False

from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import pickle as pk

from user import *

from friends_frame import FriendsFrame
from analysis_health_frame import AnalysisFrame

from add_content import AddContent
from view_content import ViewContent
from add_request import AddRequest # [추가]
from view_request import ViewRequest # [추가]
from connect_doctor import ConnectDoctorFrame # [추가]

class ChangePasswordFrame(Frame): # 비밀번호 변경 프레임
    def __init__(self, frame: Frame, user: User):
        super().__init__(window, bg = "#09FFFA", width = 800, height = 800)
        self.__user = user

        self.closeFrameButton = Button(self, text = '<', bg = '#09FFFA', font = ('Arial', 15, 'bold'), borderwidth = 0, command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 10, y = 10)

        self.titleLabel = Label(self, text = '비밀번호 변경', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.titleLabel.place(x = 270, y = 75)

        self.idLabel = Label(self, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.currentPasswordLabel = Label(self, text = '현재 비밀번호', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.changedPasswordLabel = Label(self, text = '새 비밀번호', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.changedPasswordAgainLabel = Label(self, text = '비밀번호 확인', font = ('Arial', 15, 'bold'), bg = '#09FFFA')

        self.myIdLabel = Label(self, text = '{}'.format(self.__user.getId()), font = ('Arial', 15, 'bold'), bg = '#09FFFA') # 사용자 아이디 정보 레이블
        self.currentPasswordEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 27)
        self.changedPasswordEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 27)
        self.changedPasswordAgainEntry = Entry(self, font = ('Arial', 15, 'bold'), bg = 'white', width = 27)

        self.idLabel.place(x = 150, y = 275); self.myIdLabel.place(x = 300, y = 275)
        self.currentPasswordLabel.place(x = 150, y = 360); self.currentPasswordEntry.place(x = 300, y = 360)
        self.changedPasswordLabel.place(x = 150, y = 445); self.changedPasswordEntry.place(x = 300, y = 445)
        self.changedPasswordAgainLabel.place(x = 150, y = 530); self.changedPasswordAgainEntry.place(x = 300, y = 530)

        self.cancelButton = Button(self, text = '취소', font = ('Arial', 14, 'bold'), bg = 'white', width = 7, command = lambda: self.closeFrame())
        self.changePasswordButton = Button(self, text = '변경', font = ('Arial', 14, 'bold'), bg = 'yellow', width = 7, command = lambda: self.changePassword())

        self.cancelButton.place(x = 295, y = 650); self.changePasswordButton.place(x = 405, y = 650)

    def changePassword(self): # 비밀번호 변경 메소드
        if self.currentPasswordEntry.get() == '':
            messagebox.showerror('오류', '현재 비밀번호가 입력되지 않았습니다.')
            return
        if self.changedPasswordEntry.get() == '':
            messagebox.showerror('오류', '새 비밀번호가 입력되지 않았습니다.')
            return
        if self.changedPasswordAgainEntry.get() == '':
            messagebox.showerror('오류', '새 비밀번호가 다시 입력되지 않았습니다.')
            return

        if self.currentPasswordEntry.get() != self.__user.getPw():
            messagebox.showerror('오류', '현재 비밀번호가 일치하지 않습니다.')
            return
        if self.changedPasswordEntry.get() == self.__user.getPw():
            messagebox.showerror('오류', '새 비밀번호가 현재 비밀번호랑 동일합니다.')
            return
        if len(self.changedPasswordEntry.get()) < 3 or len(self.changedPasswordEntry.get()) > 12:
            messagebox.showerror('오류', '비밀번호의 길이는 3~12자로 입력하세요.')
            return
        if self.changedPasswordEntry.get() != self.changedPasswordAgainEntry.get():
            messagebox.showerror('오류', '다시 입력된 새 비밀번호가 일치하지 않습니다.')
            return

        userlistFile = open('..//Datas//userlist.bin', mode = 'rb')
        userlist: list[User] = pk.load(file = userlistFile)
        userlistFile.close()

        for i in range(len(userlist)):
            if userlist[i].getId() == self.__user.getId():
                userlist[i].setPw(self.changedPasswordEntry.get())
                break

        userlistFile = open('..//Datas//userlist.bin', mode = 'wb')
        pk.dump(file = userlistFile, obj = userlist)
        userlistFile.close()

        messagebox.showinfo('알림', '비밀번호 변경이 완료되었습니다.')
        self.closeFrame()

    def closeFrame(self): # 현재 창을 닫는 메소드
        self.place_forget()


class MainFrame(Frame, User):
    def openMainFrame(self) -> None:
        mainFrame = Tk()
        mainFrame.geometry('800x800')

        """
        loginFrame = LoginFrame()
        assignFrame = AssignFrame()
        """

        mainFrame.mainloop()

    def open_add_content_window(self):
        # 의사용: 콘텐츠 추가 창
        new_window = Toplevel(self)
        new_window.title("콘텐츠 추가")
        new_window.geometry("800x800")
        
        frame = AddContent(new_window)
        frame.pack(fill="both", expand=True)

    # 환자용: 콘텐츠 조회 창 열기
    def open_view_content_window(self):
        self.viewContentFrame = ViewContent(self, self.user.getId())
        self.viewContentFrame.place(x = 0, y = 0)

    # 환자용: 건강 데이터 분석 창 열기
    def openAnalysisFrame(self):
        self.analysisFrame = AnalysisFrame(self, self.user)
        self.analysisFrame.place(x = 0, y = 0)

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

    # [추가] 환자용: 친구 목록 및 경쟁 창 열기
    def openFriedsFrame(self):
        self.friendsFrame = FriendsFrame(self, self.user)
        self.friendsFrame.place(x = 0, y = 0)

    # [추가] 환자용: 주치의 연결 창 열기
    def openConnectDoctorFrame(self):
        self.connectDoctorFrame = ConnectDoctorFrame(self, self.user)
        self.connectDoctorFrame.place(x = 0, y = 0)

    # [추가] 비밀번호 변경 창 열기
    def openChangePasswordFrame(self):
        self.changePasswordFrame = ChangePasswordFrame(self, self.user)
        self.changePasswordFrame.place(x = 0, y = 0)

    def __init__(self, window: Frame, user: User) -> None:
        super().__init__(window, bg = "#09FFFA", width = 800, height = 800)

        self.user = user

        self.mainTitleLabel = Label(self, text = '메인 메뉴', font = ('Arial', 30, 'bold'), bg = '#09FFFA')
        self.mainTitleLabel.place(x = 300, y = 50)


        self.menuLabel_1 = Label(self, text = '건강 데이터', font = ('Arial', 12, 'bold'), bg = "#E6FF09")
        self.menuLabel_1.place(x = 105, y = 140)

        self.F1A1_Button = Button(self, text = '건강 데이터 분석', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1, command = lambda: self.openAnalysisFrame())
        self.F1A1_Button.place(x = 85, y = 200)

        """
        self.F1A2_Button = Button(self, text = '건강 데이터 조회', font = ('Arial', 8, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A2_Button.place(x = 150, y = 210)
        """

        self.F1B_Button = Button(self, text = '위험도 조회', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1B_Button.place(x = 85, y = 240)

        self.F1C1_Button = Button(self, text = '개인 리포트', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1C1_Button.place(x = 85, y = 280)

        self.F1C2_Button = Button(self, text = '알림 설정', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1C2_Button.place(x = 85, y = 320)

        self.F1A3_Button = Button(self, text = '식단 기록', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A3_Button.place(x = 85, y = 360)

        self.F1A4_Button = Button(self, text = '식단 추천', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F1A4_Button.place(x = 85, y = 400)


        self.menuLabel_2 = Label(self, text = '콘텐츠', font = ('Arial', 12, 'bold'), bg = "#E6FF09")
        self.menuLabel_2.place(x = 290, y = 140)

        self.F2A_Button = Button(self, text = '친구 관리', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1, command = lambda: self.openFriedsFrame())
        self.F2A_Button.place(x = 250, y = 200)

        self.F2B_Button = Button(self, text = '배지 개수 확인', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F2B_Button.place(x = 250, y = 240)

        self.F3B_Button = Button(self, text = '콘텐츠 확인', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1, command = lambda: self.open_view_content_window())
        self.F3B_Button.place(x = 250, y = 280)


        self.F3A_Button = Button(self, text = '콘텐츠 관리', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3A_Button.place(x = 250, y = 320)
        self.F3A_Button.config(command = self.open_add_content_window)
        

        self.F3D2_Button = Button(self, text = '콘텐츠 변경 요청', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3D2_Button.place(x = 250, y = 360)
        self.F3D2_Button.config(command = self.open_request_change_window)

        self.F3D2_1_Button = Button(self, text = '변경 요청 확인', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F3D2_1_Button.place(x = 250, y = 400)
        self.F3D2_1_Button.config(command = self.open_view_requests_window)

        self.menuLabel_3 = Label(self, text = '환자 관리', font = ('Arial', 12, 'bold'), bg = "#E6FF09")
        self.menuLabel_3.place(x = 445, y = 140)

        self.F4A_Button = Button(self, text = '환자 패널 보기', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F4A_Button.place(x = 415, y = 200)


        self.menuLabel_4 = Label(self, text = '개인정보 관리', font = ('Arial', 12, 'bold'), bg = "#E6FF09")
        self.menuLabel_4.place(x = 590, y = 140)

        self.F5P_Button = Button(self, text = '비밀번호 재설정', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1, command = lambda: self.openChangePasswordFrame())
        self.F5P_Button.place(x = 580, y = 200)

        self.F5C_Button = Button(self, text = '가족 공유 연결', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1)
        self.F5C_Button.place(x = 580, y = 240)

        self.F5D_Button = Button(self, text = '주치의 연결', font = ('Arial', 12, 'bold'), bg = 'white',\
                width = 12, activebackground = '#09FFFA', borderwidth = 1, command = lambda: self.openConnectDoctorFrame())
        self.F5D_Button.place(x = 580, y = 280)

        self._config_button()

    def _config_button(self):
        user_type = self.user.getUserType()

        if user_type == '개인 사용자': 
                self.F4A_Button.config(state = DISABLED)
                self.F3A_Button.config(state = DISABLED)
                self.F3D2_1_Button.config(state = DISABLED)
                
        elif user_type == '주치의': 
              self.F1A1_Button.config(state = DISABLED)
              # self.F1A2_Button.config(state = DISABLED)
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
        elif user_type == '보호자':
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



if DEBUG:
    window = Tk()
    window.geometry('800x800')

    patient = Patient('ABC', 10, '남', 'uk3181', '1234', '010-9494-5836', 'uk3181@daum.net', '개인 사용자')
    data = Data(1000, 10, 10, [10, 10], 1, True, True, 1, 1, 1, 1)
    patient.addData(data)
    patient.addData(Data(year = 2025, month = 11, day = 16, carboKcal = 1000, proteinKcal = 2000, fatKcal = 1000))

    """
    doctor = Doctor('김의사', 40, '남', 'doc123', 'doc123@', '010-1234-5678',\
        'uk3181@naver.com', '주치의')
    """

    frame = MainFrame(window, patient)
    frame.place(x = 0, y = 0)

    window.mainloop()

if DEBUG_FOR_PASSWORD_FRAME:
    window = Tk()
    window.geometry('800x800')

    doctor = Doctor('김의사', 40, '남', 'doc123', 'doc123@', '010-1234-5678',\
        'uk3181@naver.com', '주치의')

    frame = ChangePasswordFrame(window, doctor)
    frame.place(x = 0, y = 0)

    window.mainloop()