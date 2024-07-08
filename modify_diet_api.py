import pathlib
import textwrap
import json
import google.generativeai as genai

# API 키
my_api_key = "AIzaSyCbMrzUXYOAg4vuDxYv5vwWQUkK6kUJIu8"

# Geminai API 키 설정
genai.configure(api_key=my_api_key)
genai.project_id = "533241448251"

def call_geminai_api(prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# 예시 데이터!! 인물 정보 받을 것!!
user_id = 1
member_info = {
    "height": 176,
    "weight": 80,
    "sex": "Male",
    "background": "No preference for seafood",
    "must_have_item": "Fried chicken, 1 time per week"
}

# 예시 데이터!! DB에서 식단 받을 것!!
meal_plan = [
  {
    "start_date": "2024-06-20",
    "meal_type": "breakfast",
    "diet": "Oatmeal with fruits"
  },
  {
    "start_date": "2024-06-20",
    "meal_type": "lunch",
    "diet": "Chicken salad"
  },
  {
    "start_date": "2024-06-20",
    "meal_type": "dinner",
    "diet": "Grilled salmon with vegetables"
  },
  {
    "start_date": "2024-06-20",
    "meal_type": "snack",
    "diet": "Yogurt with granola"
  },
  {
    "start_date": "2024-06-21",
    "meal_type": "breakfast",
    "diet": "Scrambled eggs with toast"
  },
  {
    "start_date": "2024-06-21",
    "meal_type": "lunch",
    "diet": "Tuna sandwich"
  },
  {
    "start_date": "2024-06-21",
    "meal_type": "dinner",
    "diet": "Chicken stir-fry"
  },
  {
    "start_date": "2024-06-21",
    "meal_type": "snack",
    "diet": "Fruit salad"
  }
]

# 예시 데이터!! 대신 먹은 음식+날짜 입력할 것!!
new_food = "fried chicken"
new_food_date = "2024-06-20"
new_food_mealtype = "dinner"

# 개인정보 변수처리
height = member_info["height"]
weight = member_info["weight"]
sex = member_info["sex"]
background = member_info["background"]
must_have_item = member_info["must_have_item"]

def update_meal_plan(meal_plan, new_food, date, new_food_mealtype):
    prompt = f"""
    I am a dietitian. My client had an existing diet, but the client ate {new_food} on {date}, {new_food_mealtype}.
    Please refer to following information and *Guidelines*, and to create a diet plan for the remaining period.
    The client is {sex}, {height} cm tall and weighs {weight} kg. They have indicated a preference for {background} and requested to include {must_have_item} in their diet. 
    
    Existing Meal Plan:
    ```json
    {json.dumps(meal_plan, indent=4)}
    ```

    **Guidelines:**
    1. Create a diet reflecting the client's preferences and needs as much as possible.
    2. "Background" and "Must have items" should be considered as much as possible unless they are fatal.
    3. The diet should be enjoyable for daily consumption while maintaining a healthy balance.
    4. The total period is from {date} {new_food_mealtype} to the last date of the original meal_plan.

    **Output format:**

    Please provide the output in a plain text format with the following structure:

    ```
    [
      {{
        "start_date": "2024-06-20",
        "meal_type": "breakfast",
        "diet": "Oatmeal with fruits"
      }},
      {{
        "start_date": "2024-06-20",
        "meal_type": "lunch",
        "diet": "Chicken salad"
      }},
      ...
    ]
    ```
    """
    updated_meal_plan = call_geminai_api(prompt)
    return updated_meal_plan

def main():
    # 업데이트된 식단 계획 출력
    updated_meal_plan = update_meal_plan(meal_plan, new_food, new_food_date, new_food_mealtype)
    print(f"업데이트된 식단 계획:\n{updated_meal_plan}")

if __name__ == "__main__":
    main()