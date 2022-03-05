import motor.motor_asyncio
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.FastChat

userAvailable_collection = database.get_collection('UserAvailable')
conversation_collection = database.get_collection('Conversation')
chat_collection = database.get_collection('Chat')