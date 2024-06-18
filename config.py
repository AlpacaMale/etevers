class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:root1234@rds.cluster-crqgcai442on.ap-northeast-2.rds.amazonaws.com/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'