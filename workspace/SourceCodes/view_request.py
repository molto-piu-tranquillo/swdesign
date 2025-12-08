from tkinter import *
from tkinter import messagebox
import pickle as pk
import os
from user import Patient

class ViewRequest(Frame):
    
    # [추가된 기능] 모든 요청 삭제하기
    def clear_all_requests(self):
        response = messagebox.askyesno("확인", "모든 요청을 확인 처리(삭제) 하시겠습니까?")
        if not response: return

        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..', 'Datas', 'userlist.bin')
        file_path = os.path.normpath(file_path)

        try:
            with open(file_path, 'rb') as f:
                userlist = pk.load(f)

            # 모든 환자의 요청함 비우기
            for user in userlist:
                # 환자 객체이고, 비우기 기능이 있는지 확인
                if (user.getUserType() == '개인 사용자' or user.getUserType() == 'Patient') \
                   and hasattr(user, 'clear_change_requests'):
                    user.clear_change_requests() # 요청 삭제

            # 변경된 내용(빈 리스트) 저장
            with open(file_path, 'wb') as f:
                pk.dump(userlist, f)
            
            # 화면 갱신 (텍스트 박스 비우기)
            self.displayObj.config(state=NORMAL)
            self.displayObj.delete("1.0", END)
            self.displayObj.insert(END, "모든 요청이 처리되었습니다.")
            self.displayObj.config(state=DISABLED)

            messagebox.showinfo("성공", "요청 목록을 초기화했습니다.")

        except Exception as e:
            messagebox.showerror("오류", f"삭제 중 오류: {e}")


    def __init__(self, window):
        super().__init__(window, bg='white', width=500, height=600)

        Label(self, text="환자 변경 요청 목록", font=('Arial', 20, 'bold'), bg='white').place(x=120, y=20)

        self.displayObj = Text(self, width=60, height=35, font=('Arial', 10), state=DISABLED, relief="solid")
        self.displayObj.place(x=30, y=80)
        
        # 닫기 버튼
        Button(self, text="닫기", font=('Arial', 12), command=window.destroy).place(x=350, y=550)

        # [추가] 확인 완료(삭제) 버튼
        Button(self, text="확인 완료 (전체 삭제)", font=('Arial', 12, 'bold'), bg='#FFB6C1', 
               command=self.clear_all_requests).place(x=100, y=550)

        self.load_all_requests()

    def load_all_requests(self):
        # ... (이 부분은 기존 코드와 동일합니다) ...
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..', 'Datas', 'userlist.bin')
        file_path = os.path.normpath(file_path)

        try:
            with open(file_path, 'rb') as f:
                userlist = pk.load(f)
            
            self.displayObj.config(state=NORMAL)
            self.displayObj.delete("1.0", END)
            
            has_request = False

            for user in userlist:
                u_type = user.getUserType()
                is_patient = (u_type == '개인 사용자' or u_type == 'Patient')

                if is_patient and hasattr(user, 'get_change_requests'):
                    requests = user.get_change_requests()
                    if requests:
                        has_request = True
                        self.displayObj.insert(END, f"■ 환자 ID: {user.getId()} ({user.getName()})\n")
                        self.displayObj.insert(END, "-" * 50 + "\n")
                        for i, req in enumerate(requests):
                            self.displayObj.insert(END, f" {i+1}. {req}\n")
                        self.displayObj.insert(END, "\n" + "=" * 50 + "\n\n")

            if not has_request:
                self.displayObj.insert(END, "들어온 변경 요청이 없습니다.")

            self.displayObj.config(state=DISABLED)

        except Exception as e:
            messagebox.showerror("오류", f"데이터 로드 중 오류: {e}")