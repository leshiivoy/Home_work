from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

users_db = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/user")
async def get_user():
    return users_db


@app.post('/user/{username}/{age}')
async def post_user(user: User, username: str, age: int):
    name = len(users_db)
    if name == 0:
        user.id = 1
    else:
        user.id = users_db[name - 1].id + 1
    user.username = username
    user.age = age
    users_db.append(user)
    return users_db


@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: int, username: str, age: int):
    try:
        users_db[user_id - 1] = User(id=user_id, username=username, age=age)
        return users_db[user_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    if user_id == users_db[user_id - 1].id:
        return users_db.pop(user_id - 1)
    else:
        raise HTTPException(status_code=404, detail="User was not found")
