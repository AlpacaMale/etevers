import redis

DB_PRIMARY_ROUTE = "172.16.0.201"
DB_SECONDARY_ROUTE = "172.16.0.202"
RDS_ROUTE = "rds.crqgcai442on.ap-northeast-2.rds.amazonaws.com"
REDIS_ROUTE = "redis-session-nhbb1i.serverless.apn2.cache.amazonaws.com"


class Config:

    SQLALCHEMY_BINDS = {
        "db_primary": f"mysql+pymysql://root:12345678@{ DB_PRIMARY_ROUTE }:3306/mydb",
        "db_secondary": f"mysql+pymysql://root:12345678@{ DB_SECONDARY_ROUTE }:3306/mydb",
        "rds": f"mysql+pymysql://root:12345678@{ RDS_ROUTE }:3306/mydb",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "flask:"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_ROUTE, port=6379, db=0)
