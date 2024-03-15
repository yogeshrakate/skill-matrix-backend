from passlib.context import CryptContext

from fastapi_mail import ConnectionConfig

SECRET_KEY = "5a7a16201e690fbac4d0bf75be666da34c0848a9181bc3b632448634aadc4111"
ENTRYPTION_KEY = b'TY1Smx4WBQvwI0ceeBtaYNI-VHdBm_41wygDHBNmME0='

JWT_TOKEN_EXPIRY_IN_MINUTES = 5

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


conf = ConnectionConfig(
   MAIL_USERNAME="skillmtrx@gmail.com",
   MAIL_PASSWORD="qdrx qrrt vexz dewl",
   MAIL_FROM="skillmtrx@gmail.com",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_STARTTLS = True,
   MAIL_SSL_TLS = False,
)

DEFAULT_ADMIN_ROUTE = "/admin"