import os
from dotenv import load_dotenv, find_dotenv
from tempfile import mkdtemp
load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    ELASTIC_USERNAME = os.getenv('ELASTIC_USERNAME')
    ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL')
    MAIL_PASSWORD = os.getenv('EMAILPASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig:
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    ELASTIC_USERNAME = os.getenv('ELASTIC_USERNAME')
    ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL')
    MAIL_PASSWORD = os.getenv('EMAILPASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
