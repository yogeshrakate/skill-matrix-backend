from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Request

from src.Api.models import User
from ..pydantic_models import *
from ..database import session as db
from ..helper import hash_password, generate_jwt_token, send_email, decrypt_link, verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@router.post("/signup")
async def user_signup(request:PydanticUser, url: Request):
    """
    Signup Api.
    """
    hashed_password = hash_password(request.password, request.confirm_password)
    if not hashed_password:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Password and Confirm Password doesn't match.",
                "data": {}
            }
        )
    user_item = request.model_dump()
    user_item.pop("confirm_password")
    user_item["password"] = hashed_password
    try:
        new_user = User(**user_item)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "message": str(e),
                "data": {}
            }
            )
    # Sending verification mail
    redirect_url = "verify-email"
    await send_email(user_item['email_address'], str(url.base_url), redirect_url)
    data_dict = {
            "message": "User Data Registered, Email verification awaited",
            "data": {
            "hashed_password": hashed_password,
            "email_address": request.email_address,
            "full_name": request.full_name,
            }
        }
    return JSONResponse(
        status_code=200,
        content= data_dict
    )

@router.get("/verify-email")
async def verify_email(url:Request):
    """
    Email Verification Api.
    """
    token = url.query_params['token']
    email = url.query_params['email']
    decrypt_data = decrypt_link(eval(token))
    if email != decrypt_data:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Verification failed.",
                "data": {}
            }
            )
    forgot = url.query_params['forgot']
    if forgot!="true":
        user = db.query(User).filter(User.email_address==email).first()
        user.is_active = True
        db.commit()
        db.refresh(user)
    data_dict = {
            "message": "Email verification successfull",
            "data": {
                "email": email
            }
        }
    return JSONResponse(
    status_code=200,
    content= data_dict
    )

@router.post("/forgot-password")
async def forgot_password_mail(data:PydanticForgotPassword, url:Request):
    """
    Forgot password Mail sender.
    """
    redirect_url = "verify-email"
    await send_email(
                    data['email_address'],
                    str(url.base_url), 
                    redirect_url, 
                    forgot="true"
                )
    data_dict = {
            "message": "Email Sent Successfully.",
            "data": {}
        }
    return JSONResponse(
    status_code=200,
    content= data_dict
    )
@router.post("/login")
async def login(request:dict):
    email = request['email']
    password = request["password"]
    user = db.query(User).filter(User.email_address==email).first()    
    if not user:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Login failed, email doesn't exist.",
                "data": {}
            }
            )
    encrypted_password = user.password
    verified_password = verify_password(password, encrypted_password)
    if not verified_password:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Login failed, incorrect password.",
                "data": {}
            }
            )
    token = generate_jwt_token({"email": email})
    data_dict = {
            "message": "Login Successful.",
            "data": {
                "access_token": token,
            }
        }
    return JSONResponse(
    status_code=200,
    content= data_dict
    )
    

@router.post("/update-password")
async def change_password(request:PydanticChangePassword):
    """
    Change password for forgot password.
    """
    hashed_password = hash_password(request.password, request.confirm_password)
    if not hashed_password:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Password and Confirm Password doesn't match.",
                "data": {}
            }
            )
    try:
        user = db.query(User).filter(User.email_address==request.email).first()
        user.password = request.password
        db.commit()
        db.refresh(user)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "message": str(e),
                "data": {}
            }
            )
    data_dict = {
            "message": "Password Changed Successfully.",
            "data": {}
        }
    return JSONResponse(
    status_code=200,
    content= data_dict
    )
