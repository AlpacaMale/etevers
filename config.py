class Config:
    SQLALCHEMY_BINDS = {
        "db": "mysql+pymysql://user:root@localhost:3306/mydb",
        "rds": "mysql+pymysql://user:root@localhost:3306/mydb",
    }
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345678@172.16.0.201:3306/mydb"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345678@10.0.200.233:3306/mydb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
