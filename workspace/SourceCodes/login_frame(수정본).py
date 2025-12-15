"""
from tkinter import *
from tkinter import messagebox
import pickle as pk


import threading         
import time               


class MainFrame(Frame):
    """실제 메인 화면 클래스 역할을 수행하는 더미 클래스"""
    def __init__(self, window: Tk) -> None:
        super().__init__(window, bg = '#09FFFA', width=800, height=800)

        Label(self, text="🌟 로그인 성공! 여기는 메인 화면 (MainFrame)입니다 🌟", 
              font=('Arial', 20), bg='lightgreen').pack(pady=50)

        Button(self, text="알람 설정하기", font=("Arial", 18), 
               command=self.open_alarm_window).pack(pady=50)

        self.place(x=0, y=0)

    def open_alarm_window(self):
        alarm_win = Toplevel(self)
        alarm_win.title("알람 설정")
        alarm_win.geometry("300x150")

        Label(alarm_win, text="몇 초 뒤에 알람을 울릴까요?", font=("Arial", 12)).pack(pady=10)

        sec_entry = Entry(alarm_win, font=("Arial", 14))
        sec_entry.pack()

        def set_alarm():
            try:
                sec = int(sec_entry.get())
                threading.Thread(target=self.run_alarm, args=(sec,), daemon=True).start()
                alarm_win.destroy()
            except ValueError:
                messagebox.showerror("오류", "정수를 입력하세요.")

        Button(alarm_win, text="설정", font=("Arial", 12), command=set_alarm).pack(pady=10)

    def run_alarm(self, seconds):
        time.sleep(seconds)
        messagebox.showinfo("알람", f"{seconds}초가 지나 알람이 울립니다!")


class AssignFrame(Frame):
    def __init__(self, window):
        super().__init__(window, bg='yellow', width=800, height=800)
        Label(self, text="여기는 회원가입 화면입니다.", font=('Arial', 20), bg='yellow').pack(pady=300)
        self.place(x=0, y=0)


def openMainFrame():
    """로그인 성공 후 MainFrame을 띄우는 함수"""
    main_root = Tk()
    main_root.title("뇌졸중 예방 시스템 - 메인 화면")
    main_root.geometry('800x800')

    MainFrame(main_root)
    
    main_root.mainloop()


class LoginFrame(Frame):
    def login(self):
        user_id = self.idEntry.get().strip()
        user_pw = self.passwordEntry.get().strip()

        if not user_id or not user_pw:
            messagebox.showerror("오류", "ID와 비밀번호를 모두 입력해주세요.")
            return

        try:
            with open("users.bin", "rb") as f:
                users = pk.load(f)
        except FileNotFoundError:
            users = {"test_id": "1234"}
            try:
                with open("users.bin", "wb") as f:
                    pk.dump(users, f)
            except Exception:
                pass
            
            messagebox.showwarning("경고", "회원 정보 파일이 없어 테스트 계정(ID: test_id, PW: 1234)이 생성되었습니다.")
            
        if user_id in users and users[user_id] == user_pw:
            messagebox.showinfo("로그인 성공", "메인 화면으로 이동합니다.")
            self.master.destroy()
            openMainFrame()
        else:
            messagebox.showerror("실패", "ID 또는 비밀번호가 일치하지 않습니다.")
    

    def openAssignFrame(self) -> None:
        newFrame = Tk()
        newFrame.geometry('800x800')

        assignFrame = AssignFrame(newFrame)
        newFrame.mainloop()

    def __init__(self, window: Frame) -> None:
        ############################### 로그인/회원가입 화면 ############################################
        super().__init__(window, bg = '#09FFFA', width = 800, height = 800)

        self.loginTitleLabel = Label(window, text = '뇌졸중 예방\n시스템', font = ('Arial', 45, 'bold'), bg = '#09FFFA')
        self.loginTitleLabel.place(x = 250, y = 200)

        self.idLabel = Label(window, text = 'ID', font = ('Arial', 15, 'bold'), bg = '#09FFFA')
        self.passwordLabel = Label(window, text = 'Password', font = ('Arial', 15, 'bold'), bg = '#09FFFA')

        self.idEntry = Entry(window, font = ('Arial', 15), width = 25)
        self.passwordEntry = Entry(window, font = ('Arial', 15), show = '●', width = 25)

        self.idLabel.place(x = 200, y = 500); self.idEntry.place(x = 330, y = 500)
        self.passwordLabel.place(x = 200, y = 600); self.passwordEntry.place(x = 330, y = 500)
        self.passwordLabel.place(x = 200, y = 600); self.passwordEntry.place(x = 330, y = 600)

        self.loginButton = Button(window, text = '로그인', font = ('Arial', 14, 'bold'), bg = 'white',
             width = 9, activebackground = '#09FFFA', borderwidth = 1, command = self.login)
             
        self.assignButton = Button(window, text = '회원가입', font = ('Arial', 14, 'bold'), bg = 'white',
             width = 9, activebackground = '#09FFFA', borderwidth = 1, command = self.openAssignFrame)

        self.loginButton.place(x = 285, y = 700)
        self.assignButton.place(x = 415, y = 700)
        ##########################################################################################################


if __name__ == "__main__":
    root = Tk()
    root.geometry("800x800")
    LoginFrame(root)
    root.mainloop()
"""