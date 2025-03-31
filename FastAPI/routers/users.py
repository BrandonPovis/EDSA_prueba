from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix = "/users", 
                   tags = ["users"],
                   responses={404:{"message": "No ausygdbausyd"}})


#Entidad user
class User (BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id= 1, name = "Brandon", surname="Povis", url= "https://Brandon.com", age= 35),
         User(id= 2, name ="Brayan", surname="Reyes", url="https://Brayan.com", age=15),
         User(id= 3, name ="Bruce", surname="Reyes", url="https://Bruce.com", age=45)]


@router.get("/usersjson")
async def usersjson ():
    return [ {"id": 1, "name" : "Brandon", "surname": "Povis","url": "https://Brandon.com", "age": "35"},
             {"id": 2,"name" : "Brayan", "surname": "Reyes","url": "https://Brayan.com", "age": "15"},
             {"id": 3,"name" : "Bruce", "surname": "Reyes","url": "https://Bruce.com", "age": "45"}
             ]


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


@router.post("/", response_model=User,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail = "El usuario ya existe")
    
    else:
        users_list.append(user)
        return { "Usuario creado exitosamente"}
    


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


          