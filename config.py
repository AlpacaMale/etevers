import os
import redis

DB_PRIMARY_ROUTE = os.getenv("DB_PRIMARY_ROUTE")
DB_SECONDARY_ROUTE = os.getenv("DB_SECONDARY_ROUTE")
DB_USER = os.getenv("DB_USER")
DB_PASSWD = os.getenv("DB_PASSWD")
RDS_ROUTE = os.getenv("RDS_ROUTE")
REDIS_ROUTE = os.getenv("REDIS_ROUTE")
SECRET_KEY = os.getenv("SECRET_KEY")


class Config:

    SQLALCHEMY_BINDS = {
        "db_primary": f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_PRIMARY_ROUTE}:3306/mydb",
        "db_secondary": f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_SECONDARY_ROUTE}:3306/mydb",
        "rds": f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{RDS_ROUTE}:3306/mydb",
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = SECRET_KEY
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "flask:"
    SESSION_REDIS = redis.StrictRedis(
        host=REDIS_ROUTE, port=6379, ssl=True, ssl_cert_reqs=None
    )
