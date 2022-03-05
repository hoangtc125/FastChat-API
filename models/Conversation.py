import datetime

from pydantic import BaseModel


class ConversationSchema(BaseModel):
    members: list[str] = []
    chats: list[str] = []
    startedAt: str = datetime.datetime.now()

