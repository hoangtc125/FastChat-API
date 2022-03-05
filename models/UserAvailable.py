import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    nickname: str = Field(...)
    startedAt: str = datetime.datetime.now()
    expiredAt: str = datetime.datetime.now() + datetime.timedelta(seconds= 300)

    class Config:
        schema_extra = {
            "example": {
                "nickname": "JohnnyShin",
            }
        }

