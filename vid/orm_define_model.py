from tortoise.models import Model
from tortoise.fields import CharField, IntField, BooleanField, DatetimeField


class User(Model):
    id = CharField(max_length=36, pk=True)
    name = CharField(max_length=50, unique=True)
    email = CharField(max_length=255, unique=True)
    is_activate = BooleanField(default=True)
    age = IntField(default=0)
    created_at = DatetimeField(auto_now_add=True)

    class Meta:
        table = "t_user"
        unique_together = ('name', 'email')
        ordering = ["-created_at"]
        indexes = [
            'email',
        ]

    def __str__(self):
        return self.name
    