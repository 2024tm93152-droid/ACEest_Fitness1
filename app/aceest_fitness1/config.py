import os

class Config:
    VERSION = os.getenv("VERSION", "v1.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = False

class TestConfig(Config):
    TESTING = True
    DEBUG = True
