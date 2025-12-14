from tkinter import *
from tkinter import messagebox
import pickle as pk
import os

class AddRequest(Frame):
    def save_request(self):
        content = self.reqText.get("1.0", END).strip()

        if not content:
            messagebox.showwarning("입력 오류", "요청할 내용을 입력하세요.")
            return

        # 경로 설정
        file_path = '..//Datas//userlist.bin'

        try:
            with open(file_path, 'rb') as f:
                userlist = pk.load(f)

            # 로그인한 본인(Patient) 찾기
            me_index = -1
            for i, user in enumerate(userlist):
                if user.getId() == self.user_id:
                    me_index = i
                    break
            
            if me_index != -1:
                # user.py 업데이트 확인
                if hasattr(userlist[me_index], 'addChangeRequest'):
                    userlist[me_index].addChangeRequest(content)
                    
                    with open(file_path, 'wb') as f:
                        pk.dump(userlist, f)
                    
                    messagebox.showinfo("성공", "변경 요청이 전송되었습니다.")
                    self.master.destroy()
                else:
                    messagebox.showerror("오류", "객체 버전이 낮아 요청을 저장할 수 없습니다.")
            else:
                messagebox.showerror("오류", "사용자 정보를 찾을 수 없습니다.")

        except Exception as e:
            messagebox.showerror("오류", f"오류 발생: {e}")

    def __init__(self, window, user_id):
        super().__init__(window, bg='white', width=400, height=500)
        self.user_id = user_id

        Label(self, text="변경 요청 보내기", font=('Arial', 20, 'bold'), bg='white').place(x=80, y=20)
        
        Label(self, text="요청 내용:", font=('Arial', 12), bg='white').place(x=30, y=80)
        self.reqText = Text(self, width=45, height=20, font=('Arial', 10), borderwidth=1, relief="solid")
        self.reqText.place(x=30, y=110)

        Button(self, text="전송하기", font=('Arial', 12, 'bold'), bg='#09FFFA', 
               command=self.save_request).place(x=150, y=420)