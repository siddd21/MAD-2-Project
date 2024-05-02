import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


# base class
class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "./database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLITE_DB_DIR, "projectdb.sqlite3"
    )
    DEBUG = True
    UPLOAD_FOLDER = "static/audios"
    SECRET_KEY = "secret_key"
    SECURITY_PASSWORD_SALT = "salt"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 3
