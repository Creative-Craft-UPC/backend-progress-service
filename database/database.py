from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()

import os

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi('1'))

database = client.CreativeCraftDB  

attempts_collection = database.get_collection("attempts")
exercice_histories_collection = database.get_collection("exercice_histories")

async def test_connection():
    try:
        await client.admin.command("ping")
        print(" Conexión exitosa a MongoDB Atlas")
    except Exception as e:
        print(" Error conectando a MongoDB:", e)
