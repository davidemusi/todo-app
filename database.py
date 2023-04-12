import os
import motor.motor_asyncio
from model import Todo

MONGO_URL = os.environ.get("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URI"))

db = client.todo
collection = db.todos

async def fetch_all_todos() -> list[Todo]:
    todos = []
    cursur = collection.find()
    async for document in cursur:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    await collection.insert_one(document)
    return document

async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document

async def fetch_one_todo(title):
    document = await collection.find_one({"title": title})
    return document

async def delete_one_todo(title):
    await collection.delete_one({"title": title})
    return True