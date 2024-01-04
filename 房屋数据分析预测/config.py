# 配置类

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:041219@localhost:3306/hourses_data"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "123456"