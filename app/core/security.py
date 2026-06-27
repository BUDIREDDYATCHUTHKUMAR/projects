import sys
import types
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
if sys.version_info >= (3, 13) and "crypt" not in sys.modules:
    sys.modules["crypt"] = types.ModuleType("crypt")
from passlib.context import CryptContext

SECRET_KEY="SECRET_SIGNING_KEY_CHANGE_THIS_IN_PRODUCTION"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)
def create_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token