from tortoise.models import Model
from tortoise.fields import CharField, DatetimeField, BooleanField


class User(Model):
    id = CharField(max_length=36, pk=True)
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=255, unique=True)
    is_activate = BooleanField(default=True)

    class Meta:
        table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
    