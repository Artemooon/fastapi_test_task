from datetime import date
from typing import Optional

from pydantic import BaseModel, validator, root_validator, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    register_date: Optional[date] = None


class UpdateUserPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str

    @root_validator
    def passwords_match(cls, values):
        print(values)
        if not values['new_password'] or (not values['new_password_confirm']) \
                or values['new_password'] != values['new_password_confirm']:
            raise ValueError('new password and new password confirm do not match')
        return values

    @validator('old_password')
    def old_password_match(cls, old_password, **kwargs):
        if not old_password:
            raise ValueError('enter old password')
        return old_password
