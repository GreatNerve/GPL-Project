# from dotenv import dotenv_values
import os
# config = dotenv_values(".env")

# MONGO_DB_URI = config.get("MONGO_DB_URI")
# MONGO_DB_NAME = config.get("MONGO_DB_NAME")

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_AUTHROIZ_DOMAIN = os.getenv("CLERK_AUTHROIZ_DOMAIN")

print(f"MongoDB Name: {MONGO_DB_NAME}")