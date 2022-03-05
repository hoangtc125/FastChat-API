from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from jose import jwt

from database.UserAvailable import (
    add_user,
    retrieve_users,
    update_user,
    delete_nickname,
)
from models.UserAvailable import (
    UserSchema,
)
from models.utils import(
    ErrorResponseModel,
    ResponseModel,
)
from .utils import(
    SECRET_KEY,
    ALGORITHM,
    pwd_context,
)

router = APIRouter()

@router.post("/", response_description="create new user by their nickname")
async def create_new_user(user: UserSchema = Body(...)):
    '''
    This API support to create new user with their nickname

    The nickname will be added successfully if it's not equal others nickname avalable now
    '''
    user = jsonable_encoder(user)
    users = await retrieve_users()

    # check this nickname was existed?
    for dt in users:
        if dt["nickname"] == user["nickname"]:
            return ErrorResponseModel("Nickname has already exist", 200, "Please choose another nickname")
    
    # create new user
    token = jwt.encode({"nickname": user["nickname"], "startedAt": user["startedAt"]}, SECRET_KEY, algorithm=ALGORITHM)
    new_user = await add_user(user)
    users = await retrieve_users()
    return ResponseModel({"user":new_user, "users":users}, token, "users data retrieved successfully")


@router.get("/", response_description="users retrieved")
async def get_users():
    '''
    This API will return all the informations of available users in system

    API will be called frequently to show user who is available now
    '''
    users = await retrieve_users()
    if users:
        return ResponseModel(users, None, "users data retrieved successfully")
    return ResponseModel(users, None, "Empty list returned")

@router.put("/{token}")
async def update_user_data(token: str):
    '''
    This API support to update expired time of the user

    API will be call frequently with input token
    '''
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    updated_user = await update_user(payload.get('nickname'))
    if updated_user:
        return ResponseModel(
            "user with nickname: {} name update is successful".format(payload.get('nickname')),
            token, 
            "user name updated successfully",
        )
    else:
        return ErrorResponseModel(
            "An error occurred",
            404,
            "There was an error updating the user data.",
        )