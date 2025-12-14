from tkinter import *
from tkinter import messagebox
import pickle as pk
from user import User

class ViewContent(Frame):
    def __init__(self, window: Frame, user_id):
        super().__init__(window, bg='white', width=800, height=800)
        self.user_id = user_id

        Label(self, text="나의 콘텐츠", font=('Arial', 20, 'bold'), bg='white').place(x=310, y=20)

        # 콘텐츠 표시 영역 (스크롤 가능한 텍스트 박스)
        self.displayObj = Text(self, width=100, height=30, font=('Arial', 10), state=DISABLED, relief="solid")
        self.displayObj.place(x=30, y=80)
        
        # 닫기 버튼
        # self.closeFrameButton = Button(self, text="닫기", font=('Arial', 12), command=window.destroy)
        self.closeFrameButton = Button(self, text="닫기", font=('Arial', 12, 'bold'), command = lambda: self.closeFrame())
        self.closeFrameButton.place(x = 680, y = 580)

        self.load_contents()

    def load_contents(self):
        try:
            with open('..//Datas//userlist.bin', 'rb') as f:
                userlist = pk.load(f)
            
            # 현재 로그인한 사용자 정보 찾기 (최신 데이터)
            me = next((u for u in userlist if u.getId() == self.user_id), None)

            if me and hasattr(me, 'getContentList'):
                contents = me.getContentList()
                
                self.displayObj.config(state=NORMAL) # 수정 가능 상태로 변경하여 텍스트 입력
                self.displayObj.delete("1.0", END)
                
                if not contents:
                    self.displayObj.insert(END, "등록된 콘텐츠가 없습니다.")
                else:
                    for i, content in enumerate(contents):
                        self.displayObj.insert(END, f"[{i+1}] --------------------------------\n")
                        self.displayObj.insert(END, f"{content}\n\n")
                
                self.displayObj.config(state=DISABLED) # 다시 읽기 전용으로 변경
            else:
                messagebox.showerror("오류", "사용자 정보를 불러올 수 없습니다.")

        except Exception as e:
            messagebox.showerror("오류", f"파일 로드 오류: {e}")

    def closeFrame(self): # 현재 창 닫기
        self.place_forget()