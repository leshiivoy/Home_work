from fastapi import FastAPI, Path, HTTPException

app = FastAPI()

users_db = {"1": "name: Example, age: 18"}


@app.get("/users")
async def get_users() -> dict:
    return users_db


@app.post("/user/{username}/{age}")
async def post_users(username: str = Path(min_length=5, max_length=20,description='Enter username', example='Vladimir'),
                    age: int = Path(ge=18, le=120, description='Enter age', example=55)) -> dict:
    current_index = str(int(max(users_db, key=int)) + 1)
    user = f"Имя: {username}, возраст: {age}"
    users_db[current_index] = user
    return {"message": f"User {current_index} is registered"}


@app.put("/user/{user_id}/{username}/{age}")
async def put_users(username: str = Path(min_length=5, max_length=20,description='Enter username', example='Vladimir'),
                    age: int = Path(ge=18, le=120, description='Enter age', example=55), user_id: int = Path(ge=0)) -> dict:
    users_db[user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"The user {user_id} is updated"}


@app.delete("/user/{user_id}")
async def delete_users(user_id: str = Path(...)):
    if user_id in users_db:
        users_db.pop(user_id)
        return {"message": f"Пользователь с ID {user_id} удален."}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")