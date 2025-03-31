from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers

app.include_router(products.router)
app.include_router(users.router)

#app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


app.mount("/Static", StaticFiles(directory = "Static"), name="Static")



@app.get("/")
async def root ():
    return "Hola mundo"

 
@app.get("/url")
async def url ():
    return { "url":"https://peyito.com/python"}

