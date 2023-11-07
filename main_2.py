from typing import Union

from fastapi import FastAPI
from databases import Database

database = Database("sqlite:///sqldb.db")
database.connect()
# await database.execute(query="CREATE TABLE todos (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name NVARCHAR)")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todo")
async def get_todos():
    query = "SELECT * FROM todos"
    return await database.fetch_all(query=query)

@app.get("/todo/{no}")
async def get_todo(no: int):
    query = "SELECT * FROM todos WHERE ID={}".format(str(no))
    return await database.fetch_one(query=query)

@app.delete("/todo/{no}")
async def del_todo(no: int):
    query = "DELETE FROM todos WHERE ID={}".format(str(no))
    return await database.execute(query=query)

@app.post("/todo")
async def create_todo(todo: str):
    query = "INSERT INTO todos (Name) VALUES('{}')".format(str(todo))
    return await database.execute(query=query)
