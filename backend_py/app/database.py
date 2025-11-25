# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file in your backend folder

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "milktea")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
