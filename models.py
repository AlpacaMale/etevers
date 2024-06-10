# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ChatbotInteraction(db.Model):
    __tablename__ = 'chatbot_interactions'

    id = db.Column(db.Integer, primary_key=True)
    interaction_type = db.Column(db.Enum('question', 'response'), nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    users_user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False, index=True)

    users_user = db.relationship('User', primaryjoin='ChatbotInteraction.users_user_id == User.user_id', backref='chatbot_interactions')



class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    meal_time = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    users_user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False, index=True)

    users_user = db.relationship('User', primaryjoin='FoodLog.users_user_id == User.user_id', backref='food_logs')


class FoodLogComment(FoodLog):
    __tablename__ = 'food_log_comments'

    comment = db.Column(db.String, nullable=False)
    food_logs_id = db.Column(db.ForeignKey('food_logs.id'), primary_key=True)



class MealPlan(db.Model):
    __tablename__ = 'meal_plan'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    users_user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False, index=True)

    users_user = db.relationship('User', primaryjoin='MealPlan.users_user_id == User.user_id', backref='meal_plans')



class MealPlanItem(db.Model):
    __tablename__ = 'meal_plan_items'

    meal_plan_id = db.Column(db.ForeignKey('meal_plan.id'), nullable=False, index=True)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    meal_time = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack'), nullable=False)
    food_item = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    meal_plan = db.relationship('MealPlan', primaryjoin='MealPlanItem.meal_plan_id == MealPlan.id', backref='meal_plan_items')


class MealPlanTracking(MealPlanItem):
    __tablename__ = 'meal_plan_tracking'

    status = db.Column(db.Enum('completed', 'missed'), nullable=False)
    actual_food_item = db.Column(db.String(255))
    meal_plan_items_id = db.Column(db.ForeignKey('meal_plan_items.id'), primary_key=True)



class MealPreference(db.Model):
    __tablename__ = 'meal_preferences'

    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(255), nullable=False)
    frequency_min = db.Column(db.Integer, nullable=False)
    frequency_max = db.Column(db.Integer, nullable=False)
    users_user_id = db.Column(db.ForeignKey('users.user_id'), nullable=False, index=True)

    users_user = db.relationship('User', primaryjoin='MealPreference.users_user_id == User.user_id', backref='meal_preferences')



class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())


class UserProfile(User):
    __tablename__ = 'user_profile'

    height = db.Column(db.Numeric(5, 2), nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    sex = db.Column(db.Enum('male', 'female'), nullable=False)
    dietary_belief = db.Column(db.String(255))
    exercise_frequency = db.Column(db.Integer, nullable=False)
    users_user_id = db.Column(db.ForeignKey('users.user_id'), primary_key=True)


class Weight(User):
    __tablename__ = 'weight'

    users_user_id = db.Column(db.ForeignKey('users.user_id'), primary_key=True, index=True)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
