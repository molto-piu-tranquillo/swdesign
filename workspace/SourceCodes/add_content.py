from tkinter import *
from tkinter import messagebox
import pickle as pk
from user import User, Patient

class AddContent(Frame):
    def save_content(self):
        target_id = self.idEntry.get()
        content = self.contentText.get("1.0", END).strip() # 텍스트 위젯 내용 가져오기

        if not target_id:
            messagebox.showwarning("입력 오류", "환자 ID를 입력하세요.")
            return
        if not content:
            messagebox.showwarning("입력 오류", "추가할 내용을 입력하세요.")
            return

        # 데이터 파일 로드 및 업데이트
        try:
            with open('..//Datas//userlist.bin', 'rb') as f:
                userlist = pk.load(f)

            target_user = None
            target_index = -1
            
            # 환자 찾기
            for i, user in enumerate(userlist):
                if user.getId() == target_id and user.getUserType() == '개인 사용자':
                    target_user = user
                    target_index = i
                    break
            
            if target_user:
                if hasattr(target_user, 'addContent'):
                    target_user.addContent(content)
                    userlist[target_index] = target_user # 리스트 업데이트

                    # 파일 저장
                    with open('..//Datas//userlist.bin', 'wb') as f:
                        pk.dump(userlist, f)
                    
                    messagebox.showinfo("성공", f"{target_id}님에게 콘텐츠를 추가했습니다.")
                    self.master.destroy() # 창 닫기
                else:
                    messagebox.showerror("오류", "해당 환자 객체 버전이 낮아 콘텐츠 기능이 없습니다.")
            else:
                messagebox.showwarning("실패", "해당 ID의 환자를 찾을 수 없습니다.")

        except FileNotFoundError:
            messagebox.showerror("오류", "데이터 파일이 없습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"저장 중 오류 발생: {e}")

    def __init__(self, window):
        super().__init__(window, bg='white', width=800, height=800)
        
        Label(self, text="콘텐츠 추가", font=('Arial', 20, 'bold'), bg='white').place(x=310, y=20)

        # 환자 ID 입력
        Label(self, text="환자 ID:", font=('Arial', 12), bg='white').place(x=30, y=80)
        self.idEntry = Entry(self, width=25, font=('Arial', 12), borderwidth=1)
        self.idEntry.place(x=100, y=80)

        # 내용 입력
        Label(self, text="내용:", font=('Arial', 12), bg='white').place(x=30, y=130)
        self.contentText = Text(self, width=100, height=15, font=('Arial', 10), borderwidth=1, relief="solid")
        self.contentText.place(x=30, y=160)

        # 저장 버튼
        Button(self, text="저장하기", font=('Arial', 12, 'bold'), bg='#09FFFA', 
               command=self.save_content).place(x=650, y=420)