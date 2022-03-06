import datetime
from fastapi import FastAPI
from database.UserAvailable import (
    userAvailable_collection,
    expired_helper,
    delete_nickname,
)
from database.Conversation import(
    delete_members
)
from routes.UserAvailable import router as UserAvailable
from routes.Conversation import router as Conversation
from fastapi_utils.tasks import repeat_every

app = FastAPI()

app.include_router(UserAvailable, tags=["User Available"], prefix="/userAvailable")
app.include_router(Conversation, tags=["Conversation"], prefix="/Conversation")

# server auto check and update available user every 3s
@app.on_event("startup")
@repeat_every(seconds = 3)  # 3s
async def remove_offline_user() -> None:
    async for user in userAvailable_collection.find():
        user = expired_helper(user)
        expiredAt = user["expiredAt"].replace("T", " ", 1)
        expiredAt = datetime.datetime.strptime(expiredAt, '%Y-%m-%d %H:%M:%S.%f')
        if datetime.datetime.now() > expiredAt: # check expired time
            # delete both user and their conversation
            if await delete_nickname(user["nickname"]): print("delete", user["nickname"])
            else: print("can't delete", user["nickname"])
            if await delete_members(user["nickname"]): print("delete conversations of", user["nickname"])
            else: print("can't delete conversations of", user["nickname"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"FastChat": "Welcome to FastChat"}