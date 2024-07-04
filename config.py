DB_PRIMARY_ROUTE = "172.16.0.201"
DB_SECONDARY_ROUTE = "172.16.0.202"
RDS_ROUTE = "rds.crqgcai442on.ap-northeast-2.rds.amazonaws.com"


class Config:
    SQLALCHEMY_BINDS = {
        "db_primary": f"mysql+pymysql://user:root@{ DB_PRIMARY_ROUTE }:3306/mydb",
        "db_secondary": f"mysql+pymysql://user:root@{ DB_SECONDARY_ROUTE }:3306/mydb",
        "rds": f"mysql+pymysql://root:12345678@{ RDS_ROUTE }:3306/mydb",
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
