from mongoengine import connect

MONGO_DB_URI = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'GPL_DB'

def init_db():
    try:
        connect(MONGO_DB_NAME, host=MONGO_DB_URI)
        print("Database connection successful")
    except ConnectionError as e:
        print(f"Database connection failed: {e}")
        raise