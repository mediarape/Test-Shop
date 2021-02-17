from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    PICPATH = environ.get('PICPATH')
    ROOT_PATH = basedir
    DBCFG = DBCFG = {
        'dbHost': "127.0.0.1",
        'dbUser': "root",
        'dbPassword': "",
        'dbName': "shop",
        'charSet': "utf8mb4"
    }