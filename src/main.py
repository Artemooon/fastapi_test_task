from fastapi import FastAPI, status, Path
from tortoise.contrib.fastapi import register_tortoise
from settings import Settings

from schemas import UserSchema, UpdateUserPasswordSchema
from services.user_base_crud import get_all_users, create_user, remove_user, update_user_password

settings = Settings()
app = FastAPI()


@app.get('/get-users-list')
async def get_all_users_view():
    print(settings.database_url)
    return await get_all_users()


@app.post('/create-user')
async def create_user_view(user: UserSchema):
    return await create_user(user)


@app.delete('/delete-user/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user_view(user_id: int = Path(None, gt=0)):
    return await remove_user(user_id)


@app.put('/update-user-password/{user_id}', status_code=status.HTTP_200_OK)
async def update_user_password_view(user_id: int, user_passwords: UpdateUserPasswordSchema):
    return await update_user_password(user_id, user_passwords)


register_tortoise(app,
                  db_url=settings.database_url,
                  modules={'models': ['models']},
                  generate_schemas=True,
                  add_exception_handlers=True
                  )
