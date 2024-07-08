import requests
import json

# Geminai API 키
GEMINAI_API_KEY = "AIzaSyDfsf7UiwEncSM8cTnRmOon5TTzZd7ZxFg"

def call_geminai_api(prompt, max_tokens=1024, temperature=0.6, top_p=0.9):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {GEMINAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "geminai-1.5",
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["text"]

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
  ...
]
