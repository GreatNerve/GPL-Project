# from dotenv import dotenv_values
import os
# config = dotenv_values(".env")

# MONGO_DB_URI = config.get("MONGO_DB_URI")
# MONGO_DB_NAME = config.get("MONGO_DB_NAME")

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

print(f"MongoDB URI: {MONGO_DB_URI}")
print(f"MongoDB Name: {MONGO_DB_NAME}")