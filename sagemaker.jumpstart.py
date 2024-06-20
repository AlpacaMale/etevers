import boto3
import json

runtime = boto3.client('runtime.sagemaker', region_name='ap-northeast-2')

endpoint_name = 'your-endpoint-name'  # 실제 엔드포인트 이름으로 변경하세요

def call_sagemaker_endpoint(prompt, parameters=None):
    input_data = {
        'inputs': prompt,
        'parameters': parameters if parameters else {}
    }
    
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(input_data)
    )
    
    result = json.loads(response['Body'].read().decode())
    return result

prompt = """
You will act as a dietitian and plan a diet for a specific person for a specified period. Please refer to the "Guidelines" and "Information" to plan a healthy diet for this person. The output must be in SQL format with the following fields: start_date (DATE), meal_type (ENUM('breakfast', 'lunch', 'dinner', 'snack')), and diet (VARCHAR(255)).

<Guidelines>
1. The daily diet should include breakfast, lunch, dinner, and snacks (if necessary).
2. The diet should be practical and enjoyable for daily consumption while maintaining a healthy balance.
3. Allow for occasional indulgences to account for the "Must have item".
4. Food preferences and the "Must have item" must be strictly observed unless they are fatal.
</Guidelines>

<Information>
Starting date: 2024-06-20
Period: 7 days
Height: 176 cm
Weight: 80 kg
Sex: Male
Food Preference: No preference for seafood
Must have item: Fried chicken, 2 times per month
Frequency of exercise: Running and health training 3 times a week
</Information>

Plan a detailed and healthy diet for the specified period, considering all the provided information and guidelines. The output should be in SQL format, where each row represents a meal for a specific date. Here is an example format:

INSERT INTO diet_plan (start_date, meal_type, diet) VALUES ('2024-06-20', 'breakfast', 'Oatmeal with fruits');
"""

parameters = {
    'max_new_tokens': 256,
    'top_p': 0.9,
    'temperature': 0.6
}

result = call_sagemaker_endpoint(prompt, parameters)
print(f"Input:\n{prompt}\n\nOutput:\n{result['generated_text']}\n\n{'='*30}\n")