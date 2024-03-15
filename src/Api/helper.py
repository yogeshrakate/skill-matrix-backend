
import jwt
import datetime
from fastapi import HTTPException, Header
from fastapi_mail import FastMail, MessageSchema
import uuid
from cryptography.fernet import Fernet
import tracemalloc

from .config import SECRET_KEY, pwd_context, ENTRYPTION_KEY, conf, JWT_TOKEN_EXPIRY_IN_MINUTES
from .database import SessionLocal


FERNET = Fernet(ENTRYPTION_KEY)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def generate_jwt_token(data:dict):
    '''
    Creating jwt token.
    '''
    data['exp'] = datetime.datetime.now(tz=datetime.timezone.utc) + \
        datetime.timedelta(minutes=JWT_TOKEN_EXPIRY_IN_MINUTES)
    token = jwt.encode(data, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token:dict):
    '''
    Decoding the token.
    '''

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    


def hash_password(password, confirm_password):
    '''
    Hash Password.
    '''
    #check password
    if password == confirm_password:
        return pwd_context.hash(password)
    return None


def verify_password(input_password, password_hash):
    '''
    Verify Hashed password with the user entered password.
    '''
    return pwd_context.verify(input_password, password_hash)


def create_link(email):
    '''
    Create Unique verification link.
    '''
    encMessage = FERNET.encrypt(email.encode())
    return encMessage

def decrypt_link(token):
    '''
    Decrypt verification link.
    '''

    decMessage = FERNET.decrypt(token).decode()
    return decMessage
    


async def send_email(email, base_url, redirect_url, forgot=""):
    '''
    Sending Email.
    '''
    encrypt = create_link(email)
    link = base_url + f"{redirect_url}?token={encrypt}&email={email}&forgot={forgot}"
    template = f"""
        <html>
            <body>
            
                <p>Email Verification Link
                <br>Click on this link to verify the email :- {link}</p>
    
            </body>
        </html>
    """
    message = MessageSchema(
       subject="Email Verification | Skill Matrix",
       recipients=[email],  # List of recipients, as many as you can pass  
       body=template,
       subtype="html"
       )
    fm = FastMail(conf)
    await fm.send_message(message)
    return True


def verify_user(authorization: str = Header(..., convert_underscores=False)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = authorization.split("Bearer ")[1]

    #token validation logic will be written here.

    return token
