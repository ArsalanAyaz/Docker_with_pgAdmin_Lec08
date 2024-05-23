# important steps

# 1- create database on Neon
# 2- create .env file for environment variable
# 3- create setting.py file for encrypting database_string/Url
# 4- create a SQLModel
# 5- create engine 
# 6- create function for creating tables in database
# 7- create function for session management
# 8- create contexmanager for app lifespan
# 9- create all enpoint functions of todo app

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from todo import setting
from typing import Annotated
from contextlib import asynccontextmanager




# 4- create a SQLModel

class Todo(SQLModel, table=True):
    
    id: int | None = Field(default=None, primary_key=True)
    content : str = Field(min_length=3, max_length=20, index=True)
    is_completed : bool = Field(default=False)
    


# 5- create engine 
# engine in one for whole application



connection_string = str(setting.Test_DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_string, pool_recycle=300, pool_size=10, echo=True)    
     

# 6- create function for creating tables in database
def create_tables():
    SQLModel.metadata.create_all(engine)

# 7- create function for session management
def get_session():
    with Session(engine) as session:
        yield session



# 8- create contexmanager for app lifespan
# Hmary App k start hony / data add(post) krny se pehly tables create krny hoty han database me
@asynccontextmanager
async def lifespan(app:FastAPI):
    print("creating tables")
    create_tables()
    print("tables created")
    yield


app : FastAPI = FastAPI(lifespan=lifespan, title="Todo app", version="1.0.0")




# 9- create all enpoint functions of todo app

@app.get("/")
def Hello():
    return "hello world!"

@app.post("/todos", response_model=Todo)
async def create_todos(todo : Todo, session:Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
    
@app.get("/alltodos", response_model=list[Todo])
async def all_todos(session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo)
    todos = session.exec(statement).all()
    return todos
    
@app.get("/todos/{id}")
async def single_todo(id:int, session=Depends(get_session)):
    # statement = select(Todo)
    todos = session.exec(select(Todo).where(Todo.id==id)).first()
    return todos
    
@app.put("/update_todos/{id}")
async def update_todo(todo : Todo, id:int, session=Depends(get_session)):
    existing_todo = session.exec(select(Todo).where(Todo.id==id)).first()

    if existing_todo :
      #  previous content         user new content(coming through todo:Todo querry-parameter)  
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed
        session.add(existing_todo) #exiting_todo mein data add krny k liye
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code=404, detail="No task found")
    
@app.delete("/delete_todos/{id}")
async def delete_todo(id: int , session: Annotated[Session, Depends(get_session)]):
    
    
    # todo = session.exec(select(Todo).where(Todo.id == id)).first
    
    todo = session.get(Todo,id)
    
    if todo:
        session.delete(todo)
        session.commit()
        # session.refresh(todo)  
        return {"Message": "Todo successfully deleted"}
    else:
        raise HTTPException(status_code=404 , detail="Task not performed")              



def start():
    uvicorn.run("todo.main:app", port= 8000, host="localhost", reload=True)