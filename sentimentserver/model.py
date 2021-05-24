from typing import Optional

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    textlist: list = Field(...)

    class Config:
        schema_extra = {
            "example": {"textlist": ["Hello I am Happy", "I am sad"]}
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
