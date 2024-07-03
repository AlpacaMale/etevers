DB_ROUTE = "172.16.0.201"
RDS_ROUTE = "rds.crqgcai442on.ap-northeast-2.rds.amazonaws.com"


class Config:
    SQLALCHEMY_BINDS = {
        "db": f"mysql+pymysql://root:12345678@{ DB_ROUTE }:3306/mydb",
        "rds": f"mysql+pymysql://root:12345678@{ RDS_ROUTE }:3306/mydb",
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
