from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2 =   OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123456"
    },
    "Peyito222" : {
        "username": "Peyito222",
        "full_name": "Brandon Povis222",
        "email": "povisbrayan@gmail.com222",
        "disabled": True,
        "password": "123456222" 
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])


    
async def current_user(token: str = Depends(oauth2)):
    user=  search_user(token)
    if not user:
        raise HTTPException( 
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail = "Credenciales de autenticacion invalidas",
            headers = {"www.Authenticate": "Bearer"})
    
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
    if not form.password == user.password: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail = "La contraseñan no es correcta")

    return {"acces_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user

