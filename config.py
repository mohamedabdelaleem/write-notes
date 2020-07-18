import os

DEBUG = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = "sqlite:///notes_and_users.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# mail config >>>

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587   
MAIL_USE_TLS = True
TESTING = False
MAIL_USERNAME = 'wri******@gmail.com'
MAIL_DEFAULT_SENDER = ("Write&Note", "wri******@gmail.com")
MAIL_PASSWORD = "*********"
