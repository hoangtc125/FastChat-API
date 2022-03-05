from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from jose import jwt

from database.Conversation import (
    add_conversation,
    retrieve_conversation,
    retrieve_conversations,
    update_conversation,
    retrieve_members,
)
from database.UserAvailable import (
    retrieve_nickname
)
from database.Chat import(
    add_chat, 
    retrieve_chat,
    update_chat,
    check_seen_chat,
)
from models.Conversation import (
    ConversationSchema,
)
from models.Chat import (
    ChatSchema,
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

@router.get("/", response_description="get all conversations which has new messages of user")
async def get_conversations_unread(token: str = None):
    '''
    This API support to get ID from all conversations of an user

    It will be called frequently to notify user which conversation has new message
    '''

    nickname = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('nickname')
    
    # check user is available?
    if not await retrieve_nickname(str(nickname)):
        return ErrorResponseModel(
            "An error occurred", 200, "{0} are not available now".format(nickname)
        )

    # find all conversation which has new message of this user
    conversations = await retrieve_conversations(str(nickname))
    conversations_noti = []
    for conversation in conversations:
        if await check_seen_chat(str(conversation["id"]), str(nickname)) and conversation not in conversations_noti:
            conversations_noti.append(conversation)

    # return
    if conversations_noti:
        return ResponseModel(
            conversations_noti,
            token, 
            "{0} you has conversations unread".format(nickname),
        )
    else:
        return ErrorResponseModel(
            "An error occurred", 200, "{0} has 0 conversation unread".format(nickname)
        )


@router.post("/{members}", response_description="create new conversation or load conversation's content")
async def make_conversation(members: str, token: str = None):
    '''
    This API support to create new conversation between 2 users or load conversation

    It will be called frequently to update message to existed conversation
    '''
    nickname = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('nickname')

    # check user or reciever is available?
    if not await retrieve_nickname(members) or not await retrieve_nickname(str(nickname)):
        return ErrorResponseModel(
            "An error occurred", 200, "{0} are not available now".format(members)
        )
    
    # load conversation's content
    conversation = await retrieve_members([nickname, members])

    if conversation: # update message status to "seen"
        chats = []
        for chat in conversation["chats"]:
            chats.append(await retrieve_chat(chat))
        chats = chats[-12:]
        for chat in chats:
            if not chat["seen"] and chat["sender"] != nickname:
                await update_chat(str(chat["id"]))
        return ResponseModel(
            {"conversation": conversation, "chats": chats},
            token, 
            "conversation was found",
        )
    else: # create a new conversation
        conversation = ConversationSchema()
        conversation = jsonable_encoder(conversation)
        conversation["members"] = [nickname, members]
        conversation = await add_conversation(conversation)
        if conversation:
            return ResponseModel(
                conversation,
                token, 
                "conversation connect to {0} was created".format(members),
            )
        else:
            return ErrorResponseModel(
                "An error occurred", 200, "conversation with nickname {0} can't create".format(payload.get('nickname'))
            )


@router.put("/{token}", response_description="update new message to new conversation")
async def update_conversation_data(token: str, chat: ChatSchema, conversationID: str = None):
    '''
    This API support to update message from user to their conversation

    Ussing to send message
    '''
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    nickname = payload.get('nickname')

    # check nickname is available?
    if not await retrieve_nickname(str(nickname)):
        return ErrorResponseModel(
            "An error occurred", 200, "{0} are not available now".format(nickname)
        )

    # find conversation
    conversation = await retrieve_conversation(conversationID)
    if not conversation: 
        return ErrorResponseModel(
            "{0}, you are enter wrong ID conversation".format(nickname),
            200,
            "Please enter exactly conversationID which you involve",
        )

    if nickname not in conversation["members"]: 
        return ErrorResponseModel(
            "{0}, you are not in this conversation".format(nickname),
            200,
            "Please enter exactly conversationID which you involve",
        )

    # create chat and update to conversation
    chat = jsonable_encoder(chat)
    chat["sender"] = nickname
    chat["conversationID"] = conversationID
    chat = await add_chat(chat)

    updated_conversation = await update_conversation(conversationID, chat["id"])

    if updated_conversation: # load conversation and update message status
        conversation = await retrieve_conversation(conversationID)
        chats = []
        for _chat in conversation["chats"]:
            chats.append(await retrieve_chat(_chat))
        chats = chats[-12:]
        for _chat in chats:
            if not _chat["seen"] and _chat["sender"] != nickname:
                await update_chat(str(_chat["id"]))
        return ResponseModel(
            {"conversation": conversation, "chats": chats},
            token, 
            "conversation with a new massage updated successfully",
        )
    else:
        return ErrorResponseModel(
            "An error occurred", 200, "conversation with nickname {0} can't update".format(payload.get('nickname'))
        )
