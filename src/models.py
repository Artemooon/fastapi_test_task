from tortoise import models, fields


class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, null=False, unique=True)
    email = fields.CharField(max_length=255, null=False, unique=True, index=True)
    password = fields.CharField(max_length=255)
    register_date = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username
