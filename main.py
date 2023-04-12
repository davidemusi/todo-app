from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo
from database import (
    fetch_all_todos,
    create_todo,
    update_todo,
    fetch_one_todo,
    delete_one_todo,
)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/todo")
async def get_all_todos():
    response = await fetch_all_todos()
    return response

@app.post("/api/todo", response_model=Todo)
async def create_todo_data(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(status_code=400, detail="Something went wrong")

@app.put("/api/todo/{title}", response_model=Todo)
async def update_todo_data(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(status_code=400, 
                        detail=f"There is no todo with that title {title}")


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title: str):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404, 
                        detail=f"There is no todo with that title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo_by_title(title: str):
    response = await delete_one_todo(title)
    if response:
        return {"message": f"Todo with title {title} deleted successfully"}
    raise HTTPException(status_code=404, 
                        detail=f"There is no todo with that title {title}")

