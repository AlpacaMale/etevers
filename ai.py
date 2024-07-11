import google.generativeai as genai
from datetime import date as dt_date

# API 키
my_api_key = "AIzaSyCbMrzUXYOAg4vuDxYv5vwWQUkK6kUJIu8"

# Geminai API 키 설정
genai.configure(api_key=my_api_key)
genai.project_id = "533241448251"


def create_meal_chain_1(user_info, preference_datas):
    height = user_info.height
    weight = user_info.weight
    sex = user_info.sex
    background = user_info.dietary_belief
    must_have_item = [preference_data.food_item for preference_data in preference_datas]
    start_date = dt_date.today()
    period = 3

    prompt = f"""
    I am a dietitian creating a meal plan for a {sex} client. They are {height} cm tall and weigh {weight} kg.
    They have indicated a preference for {background} and requested to include {must_have_item} in their diet.

    Please create a detailed meal plan for a period of {period} days, starting from {start_date}.

    Guidelines:

    The daily diet should include breakfast, lunch, dinner, and snacks.
    "Background" and "Must have items" should be considered as much as possible unless they are fatal.
    The diet should be enjoyable for daily consumption while maintaining a healthy balance.
    Include the quantity of each food item in the description (e.g., "50 grams of spinach", "A plate of risotto").
    Each meal description should list components separated by "/". For example, "Tofu scramble with onions and mushrooms / Whole-wheat toast / A glass of soy milk".
    Do not include any notes or explanations in the output.
    Do not include markdown language in the output.
    Ensure the meal plan covers the entire specified period, not just one day.

    Output format:

    [
    {{
    "date": "YYYY-MM-DD",
    "meal_type": "breakfast",
    "diet": "Description of the meal components separated by /"
    }},
    {{
    "date": "YYYY-MM-DD",
    "meal_type": "lunch",
    "diet": "Description of the meal components separated by /"
    }},
    {{
    "date": "YYYY-MM-DD",
    "meal_type": "dinner",
    "diet": "Description of the meal components separated by /"
    }},
    {{
    "date": "YYYY-MM-DD",
    "meal_type": "snack",
    "diet": "Description of the meal components separated by /"
    }}
    ...
    ]
    """

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def create_meal_chain_2(response1):

    prompt = f"""
    You will receive a meal plan in the following format:

    [
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "breakfast",
        "diet": "Description of the meal"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "lunch",
        "diet": "Description of the meal"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "dinner",
        "diet": "Description of the meal"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "snack",
        "diet": "Description of the meal"
      }}
    ]

    For each meal, break down the "diet" description into individual components. Each component should be listed separately.

    **Guidelines:**

    1. Retain the date and meal_type for each component.
    2. Each component should be a separate entry in the output list.
    3. Do not include any notes or explanations in the output.
    4. Do not include markdown language in the output.

    **Output format:**

    [
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "breakfast",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "breakfast",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "lunch",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "lunch",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "dinner",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "dinner",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "snack",
        "diet": "Description of the meal component"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "snack",
        "diet": "Description of the meal component"
      }}
    ]

    ** data **

    {response1}

    """

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def create_meal_chain_3(response2):

    if not response2:
        return "oops! someting is wrong!!"

    prompt = f"""
    You will receive a meal plan with individual meal components in the following format:

    [
      {{
        "date": "2024-07-08",
        "meal_type": "breakfast",
        "diet": "Tofu scramble with onions and mushrooms."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "breakfast",
        "diet": "Whole-wheat toast."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "breakfast",
        "diet": "A glass of soy milk."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "lunch",
        "diet": "Quinoa salad with chickpeas."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "lunch",
        "diet": "Cucumber."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "lunch",
        "diet": "Tomatoes."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "lunch",
        "diet": "A lemon vinaigrette."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "dinner",
        "diet": "Grilled salmon."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "dinner",
        "diet": "Steamed broccoli."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "dinner",
        "diet": "Brown rice."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "snack",
        "diet": "Greek yogurt."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "snack",
        "diet": "Honey."
      }},
      {{
        "date": "2024-07-08",
        "meal_type": "snack",
        "diet": "Mixed berries."
      }}
    ]

    Translate the "diet" descriptions into Korean while retaining the date and meal_type for each component.


    **Guidelines:**

    1. Do not include any notes or explanations in the output.
    2. Do not include markdown language in the output.

    **Output format:**

    [
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "breakfast",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "breakfast",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "lunch",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "lunch",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "dinner",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "dinner",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "snack",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }},
      {{
        "date": "YYYY-MM-DD",
        "meal_type": "snack",
        "diet": "식단 구성 요소에 대한 한글 설명"
      }}
    ]


    ** data **

    {response2}

    """

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def create_meal_chain_4(response2):

    prompt = f"""
    Translate the text into Korean.
    {response2}

    """

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
