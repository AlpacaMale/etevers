class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user1:root@localhost/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'