from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "jaksniubcais"


router = APIRouter()

oauth2 =   OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"]) 

class User (BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB (User):
    password: str

users_db = {
    "Peyito" : {
        "username": "Peyito",
        "full_name": "Brandon Povis",
        "email": "povisbrayan@gmail.com",
        "disabled": False,
        "password": "$2a$12$kkgm9O7OMn8R0duc0KbEpOZDyarKo.tXP4nyvqNJWbmpFgTV69Huq"
    },
    "Peyito222" : {
        "username": "Peyito222",
        "full_name": "Brandon Povis222",
        "email": "povisbrayan@gmail.com222",
        "disabled": True,
        "password": "$2a$12$LllS4hxXc0RU6ER3OROb1ekycJJMxwn10tAaLmErhNV1WvI3.PWBe" 
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str =Depends(oauth2)):     
    
    exception = HTTPException( 
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail = "Credenciales de autenticacion invalidas",
            headers = {"www.Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")         
        if username is None:
            raise exception
    except JWTError:
        raise Exception
    return search_user(username)      
        
async def current_user(user: User = Depends(auth_user)):

    if user.disabled:
        raise HTTPException( 
            status_code= status.HTTP_400_BAD_REQUEST, 
            detail = "Usuario inactivo")    
    return user    



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail = "El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password): 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail = "La contraseñan no es correcta")
    
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION  )
    access_token = {"sub" : user.username, "exp": expire}


    return {"acces_token": jwt.encode(access_token, SECRET ,algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/login/me")
async def me(user:User = Depends(current_user)):
    return user

 