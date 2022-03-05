import datetime
from bson.objectid import ObjectId
from .config import userAvailable_collection

# helpers


def user_helper(user) -> dict:
    return {
        # "id": str(user["_id"]),
        "nickname": user["nickname"],
    }

def expired_helper(user) -> dict:
    return {
        # "id": str(user["_id"]),
        "nickname": user["nickname"],
        "expiredAt": user["expiredAt"],
    }


# crud operations


# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in userAvailable_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await userAvailable_collection.insert_one(user_data)
    new_user = await userAvailable_collection.find_one({"_id": user.inserted_id})
    return expired_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await userAvailable_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

# Retrieve a user with a matching available nickname
async def retrieve_nickname(nickname: str) -> dict:
    user = await userAvailable_collection.find_one({"nickname": nickname})
    if user:
        return user_helper(user)
    return None


# Update a user with a matching nickname
async def update_user(nickname: str):
    # Return false if an empty request body is sent.
    user = await userAvailable_collection.find_one({"nickname": nickname})
    if user:
        expiredAt = datetime.datetime.now() + datetime.timedelta(seconds= 60)
        updated_user = await userAvailable_collection.update_one(
            {"_id": ObjectId(user["_id"])}, {"$set": { "expiredAt": str(expiredAt) }}
        )
        if updated_user:
            return True
        return False
    else:
        return None

    
# Delete a user from the database based on nickname
async def delete_nickname(nickname: str):
    user = await userAvailable_collection.find_one({"nickname": nickname})
    if user:
        await userAvailable_collection.delete_one({"nickname": nickname})
        return True
    return False

