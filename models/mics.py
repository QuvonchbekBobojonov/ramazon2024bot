from models.base import BaseModel
from peewee import *


class User(BaseModel):
    chat_id = CharField(unique=True)
    region = CharField(null=True)

    class Meta:
        table_name = 'users'

    def __str__(self):
        return self.chat_id

    def __repr__(self):
        return self.chat_id

    @classmethod
    def get_user(cls, chat_id):
        return cls.get_or_none(cls.chat_id == chat_id)


class Taqvim(BaseModel):
    img = CharField()
    date = DateField()
    region = CharField()

    class Meta:
        table_name = 'taqvim'

    @classmethod
    def get_taqvim(cls, region, date):
        return cls.get_or_none((cls.region == region) & (cls.date == date))
