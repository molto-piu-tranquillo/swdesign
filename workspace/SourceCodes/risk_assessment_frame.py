"""Risk assessment frame using local persistence.

This module provides a Tkinter frame that collects stroke risk inputs,
calculates a probability with a simple fallback model, and stores the
result per user under ``Datas/risk.bin``.
"""
from datetime import datetime
import pickle as pk
from math import exp
from pathlib import Path
from tkinter import *
from tkinter import ttk, messagebox


DATA_DIR = Path(__file__).resolve().parents[2] / "Datas"
RISK_BIN = DATA_DIR / "risk.bin"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_risks() -> dict:
    _ensure_data_dir()
    if not RISK_BIN.exists():
        return {}
    try:
        with RISK_BIN.open("rb") as file:
            return pk.load(file)
    except Exception:
        return {}


def _save_risks(data: dict) -> None:
    _ensure_data_dir()
    with RISK_BIN.open("wb") as file:
        pk.dump(data, file)


def _user_key(user) -> str:
    """Return the best effort identifier for the provided user object."""
    for getter in ("getId", "getEmail", "getName"):
        if hasattr(user, getter):
            value = getattr(user, getter)()
            if value:
                return str(value)
    for attr in ("id", "email", "name"):
        if hasattr(user, attr):
            value = getattr(user, attr)
            if value:
                return str(value)
    return f"user_{id(user)}"


def _fallback_prob(age: int, hypertension: int, heart_disease: int,
                   avg_glucose_level: float, bmi: float) -> float:
    """Simple logistic model used when no external model is available."""
    z_value = (
        0.03 * age
        + 0.9 * hypertension
        + 1.1 * heart_disease
        + 0.012 * avg_glucose_level
        + 0.05 * bmi
        - 7.0
    )
    return 1.0 / (1.0 + exp(-z_value))


class RiskAssessmentFrame(Frame):
    """Frame providing stroke risk calculation and storage."""

    def __init__(self, window: Frame, current_user):
        super().__init__(window, bg="#09FFFA", width=800, height=800)
        self.__window = window
        self.__user = current_user
        self.__user_key = _user_key(current_user)

        self.__build_ui()
        self.__prefill_if_exists()

    def __build_ui(self) -> None:
        label_font = ("Arial", 13, "bold")

        Label(self.__window, text=f"사용자: {self.__user_key}", font=("Arial", 16, "bold"),
              bg="#09FFFA").place(x=40, y=40)

        Label(self.__window, text="나이 (age)", font=label_font, bg="#09FFFA").place(x=80, y=120)
        self.age_var = StringVar()
        Entry(self.__window, textvariable=self.age_var, width=20).place(x=300, y=120)

        Label(self.__window, text="고혈압 (hypertension)", font=label_font, bg="#09FFFA").place(x=80, y=180)
        self.hypertension_var = StringVar(value="0")
        ttk.Combobox(self.__window, textvariable=self.hypertension_var, values=["0", "1"],
                     width=18, state="readonly").place(x=300, y=180)

        Label(self.__window, text="심장 질환 (heart_disease)", font=label_font, bg="#09FFFA").place(x=80, y=240)
        self.heart_disease_var = StringVar(value="0")
        ttk.Combobox(self.__window, textvariable=self.heart_disease_var, values=["0", "1"],
                     width=18, state="readonly").place(x=300, y=240)

        Label(self.__window, text="평균 혈당 (avg_glucose_level, mg/dL)", font=label_font,
              bg="#09FFFA").place(x=80, y=300)
        self.avg_glucose_level_var = StringVar()
        Entry(self.__window, textvariable=self.avg_glucose_level_var, width=20).place(x=360, y=300)

        Label(self.__window, text="BMI (체질량 지수)", font=label_font, bg="#09FFFA").place(x=80, y=360)
        self.bmi_var = StringVar()
        Entry(self.__window, textvariable=self.bmi_var, width=20).place(x=300, y=360)

        Button(self.__window, text="위험도 계산 및 저장", font=("Arial", 13, "bold"), bg="white",
               command=self.__on_calc).place(x=280, y=440)

        self.result_label = Label(self.__window, text="결과: -", font=("Arial", 13, "bold"), bg="#09FFFA")
        self.result_label.place(x=80, y=520)

    def __prefill_if_exists(self) -> None:
        data = _load_risks()
        entry = data.get(self.__user_key)
        if not entry:
            return

        self.age_var.set(str(entry.get("age", "")))
        self.hypertension_var.set(str(entry.get("hypertension", "0")))
        self.heart_disease_var.set(str(entry.get("heart_disease", "0")))
        self.avg_glucose_level_var.set(str(entry.get("avg_glucose_level", "")))
        self.bmi_var.set(str(entry.get("bmi", "")))

        prob = entry.get("prob")
        score = entry.get("score")
        updated_at = entry.get("updated_at", "")
        if prob is not None and score is not None:
            self.result_label.config(
                text=f"결과: 확률={prob:.3f} (점수 {score:.1f}/10) — {updated_at}"
            )

    def __on_calc(self) -> None:
        try:
            age = int(self.age_var.get())
            hypertension = int(self.hypertension_var.get())
            heart_disease = int(self.heart_disease_var.get())
            avg_glucose_level = float(self.avg_glucose_level_var.get())
            bmi = float(self.bmi_var.get())
        except ValueError:
            messagebox.showwarning("입력 오류", "숫자 필드를 확인하세요.")
            return

        prob = _fallback_prob(age, hypertension, heart_disease, avg_glucose_level, bmi)
        prob = max(0.0, min(1.0, prob))
        score = round(prob * 10.0, 1)
        label = "High" if prob >= 0.5 else "Low"

        record = {
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "avg_glucose_level": avg_glucose_level,
            "bmi": bmi,
            "prob": prob,
            "score": score,
            "label": label,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        data = _load_risks()
        data[self.__user_key] = record
        _save_risks(data)

        self.result_label.config(
            text=f"결과: 확률={prob:.3f} (점수 {score:.1f}/10) — 저장 완료"
        )
        messagebox.showinfo("저장", "위험도 계산 결과를 저장했습니다.")


if __name__ == "__main__":
    root = Tk()
    root.geometry("800x800")
    root.configure(bg="#09FFFA")

    class DummyUser:
        def __init__(self):
            self.id = "demo_user_001"
            self.email = "demo@example.com"
            self.name = "Demo"

    frame = RiskAssessmentFrame(root, DummyUser())
    frame.place(x=0, y=0)

    root.mainloop()
