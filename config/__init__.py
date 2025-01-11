from dotenv import dotenv_values

config = dotenv_values(".env")

MONGO_DB_URI = config.get("MONGO_DB_URI")
MONGO_DB_NAME = config.get("MONGO_DB_NAME")