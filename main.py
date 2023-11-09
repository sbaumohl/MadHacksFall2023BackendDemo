from databases import Database
from fastapi import Depends, FastAPI

app = FastAPI()


# dependency injection for database connection
async def get_db():
    database = Database("sqlite:///sqldb.db")
    database.connect()
    yield database
    database.disconnect()

# Simple Easy Way to create a new table
# @app.get("/init")
# async def init():
#     await database.execute(query="CREATE TABLE todos (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name NVARCHAR)")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/todo")
async def get_todos(database: Depends(get_db)):
    query = "SELECT * FROM todos"
    return await database.fetch_all(query=query)


@app.get("/todo/{no}")
async def get_todo(no: int, database: Depends(get_db)):
    query = "SELECT * FROM todos WHERE ID={}".format(str(no))
    return await database.fetch_one(query=query)


@app.delete("/todo/{no}")
async def del_todo(no: int, database: Depends(get_db)):
    query = "DELETE FROM todos WHERE ID={}".format(str(no))
    return await database.execute(query=query)


@app.post("/todo")
async def create_todo(todo: str, database: Depends(get_db)):
    query = "INSERT INTO todos (Name) VALUES('{}')".format(str(todo))
    return await database.execute(query=query)


@app.get("/stats")
async def get_stats(database: Depends(get_db)):
    return await database(query="SELECT COUNT(*) FROM todos;")
