from fastapi import FastAPI, Path


app = FastAPI()


@app.get("/user/{user_id}")
async def Get_Main_Page(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=12)) -> dict:
    return {"message": "Вы вошли как пользователь № 12"}


@app.get("/user/{username}/{age}")
async def Get_Main_Page(username: str = Path(min_length=5, max_length=20,description='Enter username', example='Oleg')
                        , age: int = Path(ge=18, le=120, description='Enter age', example=55)) -> dict:
    return {"message": f"Информация о пользователе. Имя: {username}, Во зраст: {age}"}