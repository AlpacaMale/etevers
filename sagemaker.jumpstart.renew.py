import boto3
import json

runtime = boto3.client('sagemaker-runtime')

# 엔드포인트 이름 입력
endpoint_name = 'your-sagemaker-endpoint-name'

prompt = """
You will act as a dietitian and plan a diet for a specific person for a specified period. The person had an existing diet but did not stick to the diet and ate different things at certain times. Your role is to plan a new diet for the remaining period after “When failed to diet”. Please refer to the "Guidelines" and "Information" to plan a healthy diet for this person. The output must be in SQL format with the following fields: start_date (DATE), meal_type (ENUM('breakfast', 'lunch', 'dinner', 'snack')), and diet (VARCHAR(255)).

<Guidelines>
1. Please refer to the "existing diet" below and the "What ate instead" to plan a new diet for the remaining period.
2. The diet should be practical and enjoyable for daily consumption while maintaining a healthy balance.
3. "Must have items" must be included a certain number of times, including existing meals and new diets.
</Guidelines>

<Information>
Starting date: 2024-06-20
Period: 7 days
When failed to diet: 2024-06-25 Dinner
What ate instead: Beer, French fries, and a hamburger
Height: 176 cm
Weight: 80 kg
Gender: Male
Food Preference: No preference for seafood
Must have item: Fried chicken, 2 times per month
Frequency of exercise: Running and health training 3 times a week
</Information>

<existing diet>
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-20', 'breakfast', 'Greek yogurt with honey and mixed berries');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-20', 'lunch', 'Grilled chicken salad with mixed greens and vinaigrette');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-20', 'dinner', 'Baked salmon with quinoa and steamed broccoli');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-20', 'snack', 'Apple slices with almond butter');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-21', 'breakfast', 'Whole grain toast with avocado and poached eggs');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-21', 'lunch', 'Turkey wrap with lettuce, tomato, and hummus');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-21', 'dinner', 'Grilled shrimp with brown rice and sautéed spinach');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-21', 'snack', 'Greek yogurt with honey and nuts');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-22', 'breakfast', 'Smoothie with banana, spinach, and protein powder');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-22', 'lunch', 'Chicken Caesar salad with whole grain croutons');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-22', 'dinner', 'Stir-fried beef with vegetables and brown rice');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-22', 'snack', 'Carrot sticks with hummus');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-23', 'breakfast', 'Oatmeal with sliced banana and chia seeds');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-23', 'lunch', 'Quinoa bowl with black beans, corn, avocado, and salsa');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-23', 'dinner', 'Grilled chicken with sweet potato and steamed green beans');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-23', 'snack', 'Mixed berries with a handful of almonds');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-24', 'breakfast', 'Scrambled eggs with spinach and whole grain toast');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-24', 'lunch', 'Tuna salad with mixed greens and balsamic dressing');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-24', 'dinner', 'Baked chicken breast with wild rice and steamed broccoli');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-24', 'snack', 'Cottage cheese with pineapple chunks');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-25', 'breakfast', 'Greek yogurt with granola and fresh berries');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-25', 'lunch', 'Grilled chicken wrap with mixed veggies and tzatziki sauce');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-25', 'dinner', 'Fried chicken with mashed potatoes and green beans');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-25', 'snack', 'Sliced bell peppers with guacamole');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-26', 'breakfast', 'Whole grain pancakes with fresh fruit and a drizzle of maple syrup');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-26', 'lunch', 'Vegetable stir-fry with tofu and brown rice');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-26', 'dinner', 'Baked cod with couscous and steamed asparagus');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-26', 'snack', 'Greek yogurt with honey and walnuts');

INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-27', 'breakfast', 'Smoothie with berries, spinach, and protein powder');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-27', 'lunch', 'Grilled chicken salad with mixed greens and vinaigrette');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-27', 'dinner', 'Grilled steak with quinoa and roasted Brussels sprouts');
INSERT INTO meal_plan_items (start_date, meal_type, diet) VALUES ('2024-06-27', 'snack', 'Apple slices with peanut butter');
</existing diet>

Plan a detailed and healthy diet plan for the specified period, considering all the provided information and guidelines.
"""

payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 256,
        "top_p": 0.9,
        "temperature": 0.6
    }
}

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=json.dumps(payload)
)

result = json.loads(response['Body'].read().decode())
generated_sql = result[0]['generated_text']

print("Generated SQL Diet Plan:")
print(generated_sql)
