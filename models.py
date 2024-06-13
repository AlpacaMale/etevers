# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class ChatbotInteraction(db.Model):
    __tablename__ = 'chatbot_interactions'

    id = db.Column(db.Integer, primary_key=True)
    interaction_type = db.Column(db.Enum('question', 'response'), nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    users_email = db.Column(db.ForeignKey('users.email'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='ChatbotInteraction.users_email == User.email', backref='chatbot_interactions')



class MealPlanItem(db.Model):
    __tablename__ = 'meal_plan_items'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    meal_time = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack'), nullable=False)
    food_item = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    meal_plan_id = db.Column(db.Integer, nullable=False)
    users_email = db.Column(db.ForeignKey('users.email'), nullable=False, index=True)
    starting_date = db.Column(db.Date, nullable=False)

    user = db.relationship('User', primaryjoin='MealPlanItem.users_email == User.email', backref='meal_plan_items')


class MealPlanTracking(MealPlanItem):
    __tablename__ = 'meal_plan_tracking'

    status = db.Column(db.Enum('yet', 'completed', 'missed'), nullable=False)
    actual_food_item = db.Column(db.String(255))
    actual_food_date = db.Column(db.Date)
    meal_plan_items_id = db.Column(db.ForeignKey('meal_plan_items.id'), primary_key=True)



class MealPreference(db.Model):
    __tablename__ = 'meal_preferences'

    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(255), nullable=False)
    frequency_min = db.Column(db.Integer, nullable=False)
    frequency_max = db.Column(db.Integer, nullable=False)
    users_email = db.Column(db.ForeignKey('users.email'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='MealPreference.users_email == User.email', backref='meal_preferences')



class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(255), primary_key=True, unique=True)
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
    users_email = db.Column(db.ForeignKey('users.email'), primary_key=True)



class WeightRecord(db.Model):
    __tablename__ = 'weight_record'

    weight = db.Column(db.Numeric(5, 2), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    id = db.Column(db.Integer, primary_key=True)
    users_email = db.Column(db.ForeignKey('users.email'), nullable=False, index=True)

    user = db.relationship('User', primaryjoin='WeightRecord.users_email == User.email', backref='weight_records')

time = ['breakfast', 'lunch', 'dinner', 'snack']

sex = ['male', 'female']