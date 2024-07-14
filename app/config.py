import os

# Configuration settings
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
