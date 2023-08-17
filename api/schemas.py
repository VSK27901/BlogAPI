from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel,Field,EmailStr
import motor.motor_asyncio
import os

#load env
load_dotenv()
client=motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db=client.blog_api

#FastAPI JSON and BSON
class PyObjectId(ObjectId):
    @classmethod
    def _get_validators_(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)
    
    @classmethod
    def _modify_schema_(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory = PyObjectId, alias = "_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra={
            "example":{
                "name":"Shyam Kishore",
                "email":"shyam@example.com",
                "password":"secret"
            }
        }

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory = PyObjectId, alias = "_id")
    name:str = Field(...)
    email:EmailStr = Field(...)

    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        schema_extra={
            "example":{
                "name":"Shyam Kishore",
                "email":"shyam@example.com",
            }
        }

