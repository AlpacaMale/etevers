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

# test 용임!! 외부 DB 연결해야 함!!
user_id = 1 
member_info = {
    "height": 176,
    "weight": 80,
    "sex": "Male",
    "background": "No preference for seafood",
    "must_have_item": "Fried chicken, 1 time per week"
}

# test 용임!! 시작날짜 입력 받아야 함!!
user_settings = {
    "start_date": "2024-06-20",
    "period": 7
}

# db값을 변수처리
height = member_info["height"]
weight = member_info["weight"]
sex = member_info["sex"]
background = member_info["background"]
must_have_item = member_info["must_have_item"]
start_date = user_settings["start_date"]
period = user_settings["period"]

# 프롬프트 
prompt = f"""
I am a dietitian creating a meal plan for a {sex} client. They are {height} cm tall and weigh {weight} kg. 
They have indicated a preference for {background} and requested to include {must_have_item} in their diet. 

Please create a detailed meal plan for a period of {period} days, starting from {start_date}. 

**Guidelines:**

1. The daily diet should include breakfast, lunch, dinner, and snacks.
2.  Create a diet reflecting the client's preferences and needs as much as possible.
3. "Background" and "Must have items" should be considered as much as possible unless they are fatal.
4. The diet should be enjoyable for daily consumption while maintaining a healthy balance.

**Output format:**

Please provide the output in JSON format with the following structure:

```json
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
]"""

# test 용임!! 결과표시 화면임!!
result = call_geminai_api(prompt)
print(f"Input:\n{prompt}\n\nOutput:\n{result}\n\n{'='*30}\n")
