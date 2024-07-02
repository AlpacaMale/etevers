class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345678@172.16.0.201:3306/mydb"
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:root1234@rds.cluster-crqgcai442on.ap-northeast-2.rds.amazonaws.com:3306/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
