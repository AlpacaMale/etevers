from datetime import timedelta
import random

food_items = [
    "국수 한 그릇",
    "김치찌개 1인분",
    "계란찜 1개",
    "고등어 구이 1토막",
    "닭갈비 1인분",
    "된장찌개 1인분",
    "떡볶이 1인분",
    "볶음밥 1인분",
    "비빔밥 1인분",
    "샌드위치 1개",
    "샐러드 1팩",
    "스테이크 100g",
    "스파게티 1인분",
    "아이스크림 1개",
    "오므라이스 1인분",
    "피자 1조각",
    "햄버거 1개",
    "닭강정 100g",
    "닭꼬치 2개",
    "김밥 2줄",
    "라면 1개",
    "빵 2개",
    "피자 1조각",
    "과일 1개",
    "요거트 1개",
    "바나나 1개",
    "사과 1개",
    "딸기 10개",
    "포도 10개",
    "귤 5개",
    "수박 1/4",
    "멜론 1/4",
    "키위 2개",
    "블루베리 100g",
    "요구르트 1개",
    "우유 1잔",
    "커피 1잔",
    "주스 1잔",
    "차 1잔",
    "물 1잔",
    "양배추 150g",
    "브로콜리 100g",
    "시금치 50g",
    "고구마 1개",
    "감자 1개",
    "토마토 2개",
    "오이 1개",
    "상추 5장",
    "파프리카 1개",
    "양파 1/2개",
]

meal_times = ["breakfast", "lunch", "dinner", "snack"]


def create_meal_plan_items(start_date):

    meal_plan_items = []

    end_date = start_date + timedelta(days=7)

    current_date = start_date
    while current_date <= end_date:
        for _ in range(10):
            meal_plan_items.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "meal_time": random.choice(meal_times),
                    "food_item": random.choice(food_items),
                }
            )
        current_date += timedelta(days=1)

    return meal_plan_items
