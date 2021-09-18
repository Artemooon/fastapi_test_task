from fastapi import HTTPException, status
from models import User
from passlib.hash import pbkdf2_sha256
from tortoise.contrib.pydantic import pydantic_model_creator

user_schema_retrieve = pydantic_model_creator(User, name='User')
user_schema_create = pydantic_model_creator(User, exclude=('register_date',), name='UserNotRo')


async def get_user_by_id(user_id: int):
    user = await User.filter(id=user_id).first()
    return user


async def get_all_users():
    return await user_schema_retrieve.from_queryset(User.all())


async def create_user(user):
    user.password = pbkdf2_sha256.hash(user.password)
    user_object = await User.create(**user.dict(exclude_unset=True))
    return await user_schema_create.from_tortoise_orm(user_object)


async def remove_user(user_id: int):
    user = await get_user_by_id(user_id)
    if user:
        await user.delete()
        return {'message': 'User successfully deleted'}

    raise HTTPException(detail='User with this id not found', status_code=status.HTTP_404_NOT_FOUND)


async def update_user_password(user_id: int, user_passwords):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(detail='User with this id not found', status_code=status.HTTP_404_NOT_FOUND)
    old_user_password = user.password
    if pbkdf2_sha256.verify(user_passwords.old_password, old_user_password):
        await User.filter(id=user.id).update(password=pbkdf2_sha256.hash(user_passwords.new_password))
        return {'message': 'Password updated'}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')
