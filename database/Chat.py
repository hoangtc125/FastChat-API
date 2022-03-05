from bson.objectid import ObjectId

from .config import chat_collection

# helpers

def seen_helper(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "sender": chat["sender"],
        "seen": bool(chat["seen"]),
    }

def chat_helper(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "sender": chat["sender"],
        "time": chat["startedAt"],
        "message": chat["message"],
        "seen": bool(chat["seen"])
    }


# crud operations


# Retrieve all chats present in the database
async def check_seen_chat(conversationID: str, nickname: str):
    chats = []
    async for chat in chat_collection.find({"conversationID": conversationID}):
        chat = seen_helper(chat)
        if not chat["seen"] and nickname != chat["sender"] and chat not in chats:
            chats.append(chat)
    return chats


# Retrieve all chats present in the database
async def retrieve_chats(nickname: str):
    chats = []
    async for chat in chat_collection.find({"sender": nickname}):
        chat = seen_helper(chat)
        if not chat["seen"] and chat not in chats:
            chats.append(chat)
    return chats


# Add a new chat into to the database
async def add_chat(chat_data: dict) -> dict:
    chat = await chat_collection.insert_one(chat_data)
    new_chat = await chat_collection.find_one({"_id": chat.inserted_id})
    return chat_helper(new_chat)


# Retrieve a chat with a matching ID
async def retrieve_chat(id: str) -> dict:
    chat = await chat_collection.find_one({"_id": ObjectId(id)})
    if chat:
        return chat_helper(chat)

# Retrieve a chat with a matching available nickname
async def retrieve_nickname(nickname: str) -> dict:
    chat = await chat_collection.find_one({"nickname": nickname})
    if chat:
        return chat_helper(chat)


# Update a chat with a matching nickname
async def update_chat(id: str):
    updated_chat = await chat_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": { "seen": True }}
    )
    return True

# Delete a chat from the database
async def delete_chat(conversationID: str):
    await chat_collection.delete_many({"conversationID": conversationID})
    return True

