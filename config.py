import redis

DB_PRIMARY_ROUTE = "172.16.0.201"
DB_SECONDARY_ROUTE = "172.16.0.202"
RDS_ROUTE = "rds.crqgcai442on.ap-northeast-2.rds.amazonaws.com"
REDIS_ROUTE = "172.16.0.51"


class Config:
    SQLALCHEMY_BINDS = {
        "db_primary": f"mysql+pymysql://root:12345678@{ DB_PRIMARY_ROUTE }:3306/mydb",
        "db_secondary": f"mysql+pymysql://root:12345678@{ DB_SECONDARY_ROUTE }:3306/mydb",
        "rds": f"mysql+pymysql://root:12345678@{ RDS_ROUTE }:3306/mydb",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = "false"
    SESSION_USE_SIGNER = "True"
    SESSION_REDIS = redis.form_url(f"redis://{ REDIS_ROUTE }:6379")
