from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel 
from db.schemas.user import user_schema
from db.models.user import User
from db.client import db_client



router = APIRouter(prefix = "/userdb", 
                   tags = ["userdb"],
                   responses={status.HTTP_404_NOT_FOUND:{"message": "No encontrado"}})



users_list = []

 
@router.get("/")
async def users():
    return users_list


#Path se usa cuando te piden solo ID
@router.get("/{id}")
async def user(id: int):
    return search_user(id)
    # users = filter(lambda user: user.id == id,users_list)
    # try:
    #     return list(users)[0]
    # except:
    #     return {"error" : "Usuario no encontrado"}
    

#Query
@router.get("/")
async def user(id: int):
    return search_user(id)


@router.post("/", response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # if type(search_user(user.id)) == User:
    #     raise HTTPException(
    #         status_code=404, detail = "El usuario ya existe")
        user_dict = dict(user)
        del user_dict["id"]

        id = db_client.local.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.local.users.find_one({"_id":id}))

        return User(**new_user)
    


@router.put("/")
async def user(user: User):
    
    found = False
    
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found=True
            return {"message": "Se ha actualizado correctamente"}
   
    if not found:
        return {"error": "No se ha actualizado el usuario"}
   

    
#lo hice solo
# @app.delete("/user/{id}")
# async def user(id:int):
#     user = search_user(id)
#     if user:
#         users_list.remove(user)
#         return {"message": "Usuario eliminado"}

#     else:
#         return {"error": "Usuario no encontrado"}

@router.delete("/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found =True
            return {"message": "Se ha eliminado el usuario correctamente"}
    if not found:
        return {"error": "No se ha encontrado el usuario"}
   



def search_user(id: int):
    users = filter(lambda user: user.id == id,users_list)
    try:
        return list(users)[0]
    except:
        return {"error" : "Usuario no encontrado"}


          