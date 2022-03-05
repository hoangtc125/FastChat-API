from bson.objectid import ObjectId
from .config import conversation_collection
from database.Chat import delete_chat

# helpers

def conversation_helper(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "members": list(conversation["members"]),
        "startedAt": conversation["startedAt"],
        "chats": conversation["chats"]
    }

def conversation_noti_helper(conversation) -> dict:
    return {
        "id": str(conversation["_id"]),
        "members": list(conversation["members"]),
    }

# crud operations


# Retrieve all conversations present in the database
async def retrieve_conversations(nickname: str):
    conversations = []
    async for conversation in conversation_collection.find():
        if nickname in conversation["members"]:
            conversations.append(conversation_noti_helper(conversation))
    return conversations


# Add a new conversation into to the database
async def add_conversation(conversation_data: dict) -> dict:
    conversation = await conversation_collection.insert_one(conversation_data)
    new_conversation = await conversation_collection.find_one({"_id": conversation.inserted_id})
    return conversation_helper(new_conversation)


# Retrieve a conversation with a matching ID
async def retrieve_conversation(id: str) -> dict:
    conversation = await conversation_collection.find_one({"_id": ObjectId(id)})
    if conversation:
        return conversation_helper(conversation)

# Retrieve a conversation with a matching available members
async def retrieve_members(members: list[str]) -> dict:
    members.sort()
    async for conversation in conversation_collection.find():
        check_data = conversation["members"]
        if all(elem in members  for elem in check_data) and all(elem in check_data  for elem in members):
            return conversation_helper(conversation)
    return False

# Update a conversation with a matching conversation with new message
async def update_conversation(conversationID: str, chatID: str):
    conversation = await conversation_collection.find_one({"_id": ObjectId(conversationID)})
    if conversation: 
        chats = conversation["chats"]
        chats.append(chatID)
        print(chats)
        updated_conversation = await conversation_collection.update_one(
            {"_id": ObjectId(conversation["_id"])}, {"$set": { "chats": list(chats)}}
        )
        if updated_conversation: return True
        else: return False
    else:
        return False


# Delete a conversation from the database
async def delete_conversation(id: str):
    conversation = await conversation_collection.find_one({"_id": ObjectId(id)})
    if conversation:
        await conversation_collection.delete_one({"_id": ObjectId(id)})
        return True

    
# Delete a conversation from the database based on members
async def delete_members(nickname: str):
    async for conversation in conversation_collection.find():
        if nickname in conversation["members"]:
            await delete_chat(str(conversation["_id"]))
            await conversation_collection.delete_one({"_id": ObjectId(conversation["_id"])})
    return True

