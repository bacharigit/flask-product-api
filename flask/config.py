import os

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")


    SQLALCHEMY_TRACK_MODIFICATIONS = False



class TestingConfig(Config):
    TESTING = True
    DB_NAME = os.getenv("TEST_DB_NAME", "store_test")



def get_database_uri(config):
    return (
        f"mysql+pymysql://"
        f"{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}/{config.DB_NAME}"
    )
