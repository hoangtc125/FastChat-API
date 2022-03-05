import datetime

from pydantic import BaseModel, Field


class ChatSchema(BaseModel):
    conversationID: str = Field(None)
    sender: str = Field(None)
    startedAt: str = datetime.datetime.now()
    message: str = Field(...)
    seen: bool = False

    class Config:
        schema_extra = {
            "example": {
                "message": "Hello world",
            }
        }

