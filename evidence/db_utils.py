from pymongo import MongoClient
from django.conf import settings

def get_db():
    client = MongoClient(host=settings.MONGO_DB_SETTINGS['HOST'], port=settings.MONGO_DB_SETTINGS['PORT'])
    db = client[settings.MONGO_DB_SETTINGS['DB_NAME']]
    return db
