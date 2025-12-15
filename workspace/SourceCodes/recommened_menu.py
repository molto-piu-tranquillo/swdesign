#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import random
from pathlib import Path
from typing import List, Dict, Any, Optional

RECIPES = [
    {"id": "r1", "name": "오트밀과 블루베리", "tags": ["breakfast", "vegetarian"],
     "calories": 350, "sodium_mg": 150, "sat_fat_g": 1.0, "fiber_g": 6,
     "ingredients": ["oats", "blueberry", "almonds", "milk"]},
    {"id": "r2", "name": "구운 연어와 퀴노아", "tags": ["lunch", "dinner", "pescatarian"],
     "calories": 600, "sodium_mg": 300, "sat_fat_g": 2.5, "fiber_g": 8,
     "ingredients": ["salmon", "quinoa", "spinach", "olive oil"]},
    {"id": "r3", "name": "닭가슴살 구이와 현미", "tags": ["lunch", "dinner"],
     "calories": 550, "sodium_mg": 400, "sat_fat_g": 1.8, "fiber_g": 6,
     "ingredients": ["chicken", "brown_rice", "broccoli"]},
    {"id": "r4", "name": "후무스와 채소 스틱", "tags": ["snack", "vegetarian"],
     "calories": 180, "sodium_mg": 120, "sat_fat_g": 0.5, "fiber_g": 4,
     "ingredients": ["chickpea", "tahini", "carrot", "cucumber"]},
    {"id": "r5", "name": "두부 야채 스터프", "tags": ["lunch", "dinner", "vegetarian"],
     "calories": 450, "sodium_mg": 250, "sat_fat_g": 1.2, "fiber_g": 7,
     "ingredients": ["tofu", "mixed_vegetables", "brown_rice"]},
    {"id": "r6", "name": "아몬드와 그릭요거트", "tags": ["breakfast", "snack"],
     "calories": 300, "sodium_mg": 80, "sat_fat_g": 1.0, "fiber_g": 3,
     "ingredients": ["almond", "greek_yogurt", "honey"]},
    {"id": "r7", "name": "렌틸콩 샐러드", "tags": ["lunch", "vegetarian"],
     "calories": 420, "sodium_mg": 220, "sat_fat_g": 0.8, "fiber_g": 12,
     "ingredients": ["lentils", "tomato", "cucumber", "olive_oil"]},
    {"id": "r8", "name": "연어 샐러드 (저염)", "tags": ["lunch", "dinner", "pescatarian"],
     "calories": 520, "sodium_mg": 200, "sat_fat_g": 2.0, "fiber_g": 6,
     "ingredients": ["salmon", "lettuce", "avocado", "lemon"]},
]

# ----------------------------
# NutritionEngine 클래스
# ----------------------------
class NutritionEngine:
    def __init__(self, recipes: List[Dict[str, Any]]):
        self.recipes = recipes

    def map_risk_to_targets(self, risk_level: str) -> Dict[str, Any]:
        """risk_level -> 일일 영양 목표 매핑 (기본값)"""
        mapping = {
            "low": {"sodium_mg": 2000, "sat_fat_pct": 0.10, "fiber_g": 25},
            "moderate": {"sodium_mg": 1800, "sat_fat_pct": 0.08, "fiber_g": 28},
            "high": {"sodium_mg": 1500, "sat_fat_pct": 0.07, "fiber_g": 30},
            "very_high": {"sodium_mg": 1200, "sat_fat_pct": 0.06, "fiber_g": 32},
        }
        return mapping.get(risk_level, mapping["moderate"])

    def filter_recipes(self,
                       allergies: Optional[List[str]] = None,
                       dislikes: Optional[List[str]] = None,
                       is_vegetarian: bool = False,
                       likes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """알레르기/기호/채식 기준으로 레시피 필터링 및 선호 정렬"""
        allergies = set([a.lower() for a in (allergies or [])])
        dislikes = set([d.lower() for d in (dislikes or [])])
        likes = set([l.lower() for l in (likes or [])])

        def bad(recipe):
            ingr = set([i.lower() for i in recipe.get("ingredients", [])])
            if allergies & ingr:
                return True
            if dislikes & ingr:
                return True
            if is_vegetarian:
                nonveg = {"chicken", "beef", "pork", "salmon", "fish"}
                if ingr & nonveg:
                    return True
            return False

        filtered = [r for r in self.recipes if not bad(r)]

        def score(recipe):
            ingr = set([i.lower() for i in recipe.get("ingredients", [])])
            return len(ingr & likes)

        filtered.sort(key=score, reverse=True)
        return filtered

    def compose_daily_menu(self,
                           targets: Dict[str, Any],
                           daily_calories: int,
                           available_recipes: List[Dict[str, Any]],
                           max_sodium: Optional[int] = None): # -> (Dict[str, Any], Dict[str, Any]):
        """
        아침/점심/저녁/간식 구성 (간단한 그리디 알고리즘)
        칼로리 분배: 아침 25%, 점심 35%, 저녁 35%, 간식 5%
        """
        if max_sodium is None:
            max_sodium = targets["sodium_mg"]

        alloc = {"breakfast": 0.25, "lunch": 0.35, "dinner": 0.35, "snack": 0.05}
        menu = {"breakfast": None, "lunch": None, "dinner": None, "snack": None}
        totals = {"calories": 0, "sodium_mg": 0, "sat_fat_g": 0.0, "fiber_g": 0}

        for meal in ["breakfast", "lunch", "dinner", "snack"]:
            target_cal = daily_calories * alloc[meal]
            low, high = target_cal * 0.8, target_cal * 1.2
            candidates = [r for r in available_recipes if meal in r.get("tags", [])]
            # 우선: 칼로리 근접도 및 낮은 나트륨 우선
            candidates = sorted(candidates, key=lambda r: (abs(r["calories"] - target_cal), r["sodium_mg"]))
            chosen = None
            for c in candidates:
                projected_sodium = totals["sodium_mg"] + c["sodium_mg"]
                if projected_sodium <= max_sodium * 1.05 and low <= c["calories"] <= high:
                    chosen = c
                    break
            # 대체: 칼로리 밴드를 만족하지 못하면 나트륨 적은 순으로 선택 (허용치 110%)
            if chosen is None and candidates:
                candidates = sorted(candidates, key=lambda r: r["sodium_mg"])
                for c in candidates:
                    if totals["sodium_mg"] + c["sodium_mg"] <= max_sodium * 1.10:
                        chosen = c
                        break
            if chosen:
                menu[meal] = chosen
                totals["calories"] += chosen["calories"]
                totals["sodium_mg"] += chosen["sodium_mg"]
                totals["sat_fat_g"] += chosen["sat_fat_g"]
                totals["fiber_g"] += chosen["fiber_g"]

        return menu, totals

    def generate_week_plan(self,
                           risk_level: str,
                           daily_calories: int = 1800,
                           allergies: Optional[List[str]] = None,
                           dislikes: Optional[List[str]] = None,
                           likes: Optional[List[str]] = None,
                           is_vegetarian: bool = False,
                           max_sodium: Optional[int] = None) -> List[Dict[str, Any]]:
        """7일치 식단 생성"""
        targets = self.map_risk_to_targets(risk_level)
        if max_sodium is None:
            max_sodium = targets["sodium_mg"]

        available = self.filter_recipes(allergies=allergies, dislikes=dislikes, is_vegetarian=is_vegetarian, likes=likes)

        week = []
        for day in range(7):
            random.shuffle(available)
            menu, totals = self.compose_daily_menu(targets, daily_calories, available, max_sodium=max_sodium)
            # 만약 일부 끼니가 비어있다면 제약 완화(허용 소금 110%)
            if any(v is None for v in menu.values()):
                menu, totals = self.compose_daily_menu(targets, daily_calories, available, max_sodium=max_sodium * 1.10)
            week.append({"day": day + 1, "menu": menu, "totals": totals, "targets": targets})
        return week

    @staticmethod
    def week_to_csv(week: List[Dict[str, Any]], path: str = "..//Datas//generated_meal_plan_week.csv") -> str:
        rows = []
        for day in week:
            d = day["day"]
            menu = day["menu"]
            totals = day["totals"]
            targets = day["targets"]
            rows.append({
                "day": d,
                "breakfast": menu["breakfast"]["name"] if menu["breakfast"] else "",
                "lunch": menu["lunch"]["name"] if menu["lunch"] else "",
                "dinner": menu["dinner"]["name"] if menu["dinner"] else "",
                "snack": menu["snack"]["name"] if menu["snack"] else "",
                "calories_total": totals["calories"],
                "sodium_mg_total": totals["sodium_mg"],
                "fiber_g_total": totals["fiber_g"],
                "sat_fat_g_total": totals["sat_fat_g"],
                "sodium_target_mg": targets["sodium_mg"],
                "fiber_target_g": targets["fiber_g"]
            })
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return path

# ----------------------------
# 유틸: CSV에서 사용자 로드 (예시)
# ----------------------------
def load_first_user(csv_path: str) -> Dict[str, Any]:
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    df = pd.read_csv(p)
    if df.shape[0] == 0:
        raise ValueError("CSV is empty")
    return df.iloc[0].to_dict()

# ----------------------------
# 메인: 예제 실행
# ----------------------------
def main():
    data_path = "/mnt/data/healthcare-dataset-stroke-data (1).csv"
    try:
        sample = load_first_user(data_path)
    except Exception as e:
        print("데이터 로드 실패: - healthy.py:198", e)
        return

    # ----------------------------
    # 위험도는 이미 계산되어 있다고 가정(risk_level) — 없으면 간단히 추정
    # ----------------------------
    if "risk_level" in sample and pd.notna(sample["risk_level"]):
        risk_level = sample["risk_level"]
    else:
        # 임시 추정 규칙(프로토타입): stroke==1 -> very_high
        # age>=75 or hypertension==1 -> high, else moderate (실사용에선 외부 엔진 사용)
        if int(sample.get("stroke", 0)) == 1:
            risk_level = "very_high"
        elif sample.get("age", 0) and float(sample.get("age", 0)) >= 75:
            risk_level = "high"
        elif int(sample.get("hypertension", 0)) == 1:
            risk_level = "high"
        else:
            risk_level = "moderate"

    # 사용자 선호(예시) — 실제로는 UI/API에서 입력 받음
    user_prefs = {
        "daily_calories": 1800,
        "allergies": [],     # ex: ["egg", "milk"]
        "dislikes": ["pork"],
        "likes": ["salmon", "oats"],
        "is_vegetarian": False,
        "max_sodium": None   # None -> risk_level 기준 사용
    }

    engine = NutritionEngine(RECIPES)
    week_plan = engine.generate_week_plan(risk_level,
                                          daily_calories=user_prefs["daily_calories"],
                                          allergies=user_prefs["allergies"],
                                          dislikes=user_prefs["dislikes"],
                                          likes=user_prefs["likes"],
                                          is_vegetarian=user_prefs["is_vegetarian"],
                                          max_sodium=user_prefs["max_sodium"])

    csv_path = engine.week_to_csv(week_plan, path="/mnt/data/generated_meal_plan_week.csv")
    print(f"Sample user id: {sample.get('id')}  inferred_risk_level: {risk_level} - healthy.py:238")
    print(f"Generated 7day meal plan saved to: {csv_path}\n - healthy.py:239")
    for day in week_plan:
        d = day["day"]
        totals = day["totals"]
        menu = day["menu"]
        print(f"Day {d}: - healthy.py:244")
        for m in ["breakfast", "lunch", "dinner", "snack"]:
            item = menu[m]["name"] if menu[m] else "—"
            print(f"{m.capitalize()}: {item} - healthy.py:247")
        print(f"Totals: {totals['calories']} kcal, {totals['sodium_mg']} mg Na, {totals['fiber_g']} g fiber\n - healthy.py:248")

if __name__ == "__main__":
    main()
