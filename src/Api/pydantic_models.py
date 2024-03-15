from pydantic import BaseModel, EmailStr
from typing import List


class PydanticUser(BaseModel):
    full_name:str
    email_address:EmailStr
    password: str
    confirm_password: str

class PydanticChangePassword(BaseModel):
    email:EmailStr
    password: str
    confirm_password: str







# Admin Pydantic Models

class PydanticProject(BaseModel):
    project_name: str

class PydanticSkill(BaseModel):
    skill_name: str

class PydanticDesignation(BaseModel):
    desg_name: str

class PydanticCompetency(BaseModel):
    comp_name: str

class PydanticPermission(BaseModel):
    name: str
    operation: str

class PydanticRole(BaseModel):
    role_name: str
    permissions: List[str]

class PydanticForgotPassword(BaseModel):
    email_address: EmailStr
