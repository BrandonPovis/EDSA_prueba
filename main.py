from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel,Field, Session, create_engine, select
from typing import List
from contextlib import asynccontextmanager

class Hero(SQLModel, table = True):
    id: int | None = Field(default =None, primary_key=True )
    name: str
    superpower: str

# Create the PostgreSQL databse and engine
rds_postgresql_url = "postgresql://rootuser:edsa123456@edsa.cr82ieywavu2.sa-east-1.rds.amazonaws.com:5432/postgres"
engine=create_engine(rds_postgresql_url,echo=True)

# Initialize the database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

#Endpoint to create a hero
@app.post("/heroes/", response_model=Hero)
def create_hero(hero:Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
    
#Endpoint to get all heroes
@app.get("/heroes/",response_model=List[Hero])
def read_heroes():
    with Session(engine) as session:
        heroes  = session.exec(select(Hero)).all()
        return heroes
    
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id:int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Heron not found")
        session.delete(hero)
        session.commit()
        return {"message": "Hero deleted successfully"}