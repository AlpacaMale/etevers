from typing import Dict, List
import json
import boto3
import re
from datetime import datetime, timedelta

# 메시지 포맷팅 함수 정의
def format_messages(messages: List[Dict[str, str]]) -> str:
    """Llama-2 채팅 모델용 메시지 포맷팅 함수."""
    prompt = []

    if messages[0]["role"] == "system":
        content = "".join(["<<SYS>>\n", messages[0]["content"], "\n<</SYS>>\n\n", messages[1]["content"]])
        messages = [{"role": messages[1]["role"], "content": content}] + messages[2:]

    for user, answer in zip(messages[::2], messages[1::2]):
        prompt.extend(["<s>", "[INST] ", user["content"].strip(), " [/INST] ", answer["content"].strip(), "</s>"])

    prompt.extend(["<s>", "[INST] ", messages[-1]["content"].strip(), " [/INST] "])

    return "".join(prompt)

# SageMaker 클라이언트 생성
sagemaker_runtime = boto3.client('sagemaker-runtime')

# 엔드포인트 이름
endpoint_name = "llama2-endpoint-2"

# 중복되지 않는 식단 생성을 위한 함수 정의
def generate_diet_plan(start_date: datetime, existing_menus: List[str]) -> List[str]:
    diet_plan = []
    for day in range(3):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime('%Y-%m-%d')
        prohibited_menus = "\n".join([f"- {menu}" for menu in existing_menus])
        
        dialog = [
            {"role": "system", "content": f"""Please create a healthy diet for 1 day by following the information and guidelines below.
Make sure the meals are varied and include different foods each day. Avoid the following menus:
{prohibited_menus}

<information>
Start date: {date_str}
Weight/Height: 67kg/177cm
gender: male
</information>
<Guidelines>
You will act as a dietitian and plan a diet. There should be four meals every day: breakfast, lunch, dinner, and snack. The output must be in SQL format with the following fields: start_date (DATE), meal_type (ENUM('breakfast', 'lunch', 'dinner', 'snack')), and diet (VARCHAR(255)).
The output must only contain SQL statements. Do not include any explanations or notes.
</Guidelines>
The output does not need to say anything other than SQL. Here is an example format:

INSERT INTO diet_plan (start_date, meal_type, diet) VALUES ('{date_str}', 'breakfast', 'Oatmeal with fruits');
INSERT INTO diet_plan (start_date, meal_type, diet) VALUES ('{date_str}', 'lunch', 'hamburger');
..."""},
            {"role": "user", "content": "Create the diet plan."}
        ]

        # 프롬프트로 메시지 포맷팅
        prompt = format_messages(dialog)

        # 모델 예측 요청을 위한 JSON 생성
        input_payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000  # 필요한 경우 최대 토큰 수를 설정
            }
        }

        # 모델 예측 수행
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(input_payload)
        )

        # 예측 결과 읽기
        response_body = response['Body'].read().decode()
        result = json.loads(response_body)

        # SQL 문만 추출
        sql_statements = re.findall(r"INSERT INTO diet_plan .*?;", result[0]["generated_text"])
        diet_plan.extend(sql_statements)
        # 기존 메뉴 목록에 추가
        existing_menus.extend(re.findall(r"VALUES \('.*?', '.*?', '(.*?)'\);", result[0]["generated_text"]))

    return diet_plan

# 시작 날짜 설정
starting_date = datetime.strptime('2024-06-07', '%Y-%m-%d')

# 기존 메뉴 목록
existing_menus = []

# 7일 단위로 식단 생성
diet_plan = generate_diet_plan(starting_date, existing_menus)

# 결과 출력
for sql in diet_plan:
    print(sql)