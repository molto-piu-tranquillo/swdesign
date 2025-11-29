# apps/desktop/ui/risk_frame.py
import os
import pickle
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox

from pathlib import Path
import sys


# 프로젝트 루트 경로를 sys.path에 추가
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

try:
    from packages.domain.risk.stroke_model import stroke_risk
    print("stroke_risk model loaded from packages.domain.risk.stroke_model")
except Exception as e:
    print("WARN: stroke_risk import failed, using fallback only:", e)
    stroke_risk = None

DATA_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "data")
RISK_BIN = os.path.join(DATA_DIR, "risk.bin")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_risks():
    _ensure_data_dir()
    if not os.path.exists(RISK_BIN):
        return {}
    try:
        with open(RISK_BIN, "rb") as f:
            return pickle.load(f)
    except Exception:
        # 파일이 깨졌거나 버전이 다르면 초기화
        return {}


def _save_risks(data: dict):
    _ensure_data_dir()
    with open(RISK_BIN, "wb") as f:
        pickle.dump(data, f)


def _user_key(user) -> str:
    """
    user.py 구조를 확정할 수 없으니, 우선순위로 id/email/name을 키로 사용.
    """
    for attr in ("id", "email", "name"):
        if hasattr(user, attr):
            val = getattr(user, attr)
            if val:
                return str(val)
    # 최후 수단
    return f"user_{id(user)}"


class RiskFrame(Frame):
    """
    current_user(로그인한 사용자 객체)를 받아 위험도 계산/저장 UI 제공
    """

    def __init__(self, master, current_user):
        super().__init__(master)
        self.master.title("위험도 산출")
        self.master.geometry("800x800")
        self.current_user = current_user
        self.user_key = _user_key(current_user)
        self._build_ui()
        self._prefill_if_exists()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 6}

        row = 0
        Label(self, text=f"사용자: {self.user_key}", font=("Arial", 11, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", **pad)
        row += 1

        Label(self, text="나이 (age)").grid(row=row, column=0, sticky="e", **pad)
        self.age = StringVar()
        Entry(self, textvariable=self.age, width=18).grid(
            row=row, column=1, sticky="w", **pad)
        row += 1

        Label(self, text="고혈압 (hypertension)").grid(
            row=row, column=0, sticky="e", **pad)
        self.hypertension = StringVar(value="0")
        ttk.Combobox(self, textvariable=self.hypertension, values=[
                     "0", "1"], width=16, state="readonly").grid(row=row, column=1, sticky="w", **pad)
        row += 1

        Label(self, text="심장 질환 (heart_disease)").grid(
            row=row, column=0, sticky="e", **pad)
        self.heart_disease = StringVar(value="0")
        ttk.Combobox(self, textvariable=self.heart_disease, values=[
                     "0", "1"], width=16, state="readonly").grid(row=row, column=1, sticky="w", **pad)
        row += 1

        Label(self, text="평균 혈당 (avg_glucose_level, mg/dL)").grid(row=row,
                                                                  column=0, sticky="e", **pad)
        self.avg_glucose_level = StringVar()
        Entry(self, textvariable=self.avg_glucose_level, width=18).grid(
            row=row, column=1, sticky="w", **pad)
        row += 1

        Label(self, text="BMI (체질량 지수)").grid(
            row=row, column=0, sticky="e", **pad)
        self.bmi = StringVar()
        Entry(self, textvariable=self.bmi, width=18).grid(
            row=row, column=1, sticky="w", **pad)
        row += 1

        self.btn_calc = Button(self, text="위험도 계산 및 저장", command=self._on_calc)
        self.btn_calc.grid(row=row, column=0, columnspan=2, pady=14)
        row += 1

        self.result_lbl = Label(self, text="결과: -", font=("Arial", 11))
        self.result_lbl.grid(
            row=row, column=0, columnspan=2, sticky="w", **pad)

        self.pack(fill="both", expand=True)

    def _prefill_if_exists(self):
        data = _load_risks()
        entry = data.get(self.user_key)
        if not entry:
            return
        # 폼 채우기
        self.age.set(str(entry.get("age", "")))
        self.hypertension.set(str(entry.get("hypertension", "0")))
        self.heart_disease.set(str(entry.get("heart_disease", "0")))
        self.avg_glucose_level.set(str(entry.get("avg_glucose_level", "")))
        self.bmi.set(str(entry.get("bmi", "")))
        # 결과 표시
        prob = entry.get("prob")
        risk = entry.get("risk")
        if prob is not None and risk is not None:
            self.result_lbl.config(
                text=f"결과: 확률={prob:.3f} (점수 {risk:.1f}/10) — {entry.get('updated_at', '')}")

    def _on_calc(self):
        try:
            age = int(self.age.get())
            hypertension = int(self.hypertension.get())
            heart_disease = int(self.heart_disease.get())
            avg_glucose_level = float(self.avg_glucose_level.get())
            bmi = float(self.bmi.get())
        except ValueError:
            messagebox.showwarning("입력 오류", "숫자 필드를 확인하세요.")
            return

        # --- 범위 체크는 기존 코드 유지 ---

        # ===== 여기부터 위험도 계산 부분 교체 =====
        if stroke_risk is not None:
            try:
                result = stroke_risk(
                    age=age,
                    hypertension=hypertension,
                    heart_disease=heart_disease,
                    avg_glucose_level=avg_glucose_level,
                    bmi=bmi,
                )
                prob = float(result.get("prob", 0.0))
                label = result.get("label", "Low")
            except Exception as e:
                print("stroke_risk 모델 실행 오류, fallback 사용:", e)
                prob = _fallback_prob(
                    age, hypertension, heart_disease, avg_glucose_level, bmi)
                label = "High" if prob >= 0.5 else "Low"
        else:
            # 모델 import 자체가 안 됐을 때
            prob = _fallback_prob(
                age, hypertension, heart_disease, avg_glucose_level, bmi)
            label = "High" if prob >= 0.5 else "Low"

        prob = max(0.0, min(1.0, prob))
        risk = round(prob * 10.0, 1)
        # ===== 여기까지 =====

        record = {
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "avg_glucose_level": avg_glucose_level,
            "bmi": bmi,
            "prob": prob,
            "score": risk,
            "label": label,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        data = _load_risks()
        data[self.user_key] = record
        _save_risks(data)

        self.result_lbl.config(
            text=f"결과: 확률={prob:.3f} (점수 {risk:.1f}/10) — 저장 완료")
        messagebox.showinfo("저장", "위험도 계산 결과를 저장했습니다.")


# def _fallback_prob(age, hypertension, heart_disease, avg_glucose_level, bmi) -> float:
#     """
#     모델이 없을 때 사용
#     """
#     #가중치
#     z = (
#         0.03 * age
#         + 0.9 * hypertension
#         + 1.1 * heart_disease
#         + 0.012 * avg_glucose_level
#         + 0.05 * bmi
#         - 7.0
#     )
#     from math import exp
#     return 1.0 / (1.0 + exp(-z))


# risk_frame.py 맨 아래쪽에 추가
if __name__ == "__main__":
    from tkinter import Tk

    # user.py에 유저 클래스 있으면 사용, 아니면 그냥 아래의 더미 데이터
    class DummyUser:
        def __init__(self):
            self.id = "demo_user_001"
            self.email = "demo@example.com"
            self.name = "Demo"

    root = Tk()
    root.title("위험도 산출 (테스트)")
    root.geometry("800x800")

    current_user = DummyUser()   # 나중에 실제 로그인한 사용자로 바꿔도 됨
    app = RiskFrame(root, current_user)

    root.mainloop()
