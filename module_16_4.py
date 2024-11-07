from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic import BaseModel
from typing import List

app = FastAPI()


users_db = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get('/users')
async def get_user() -> List[User]:
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
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def put_user(id: int, username: str, age: int, user: str = Body()):
    result = True
    for edit_user in users_db:
        if edit_user.id == id:
            edit_user.username = username
            edit_user.age = age
            return edit_user
    if result:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete('/user/{id}')
async def del_user(id: int):
    result = True
    ind_del = 0
    for delete_user in users_db:
        if delete_user.id == id:
            users_db.pop(ind_del)
            return delete_user
        ind_del += 1
    if result:
        raise HTTPException(status_code=404, detail='User not found')
