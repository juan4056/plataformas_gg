import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=120)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_ingresos(self):
        return Ingreso.select().where(Ingreso.user == self)

    def get_gastos(self):
        return Gasto.select().where(Gasto.user == self)


    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
            )
        except IntegrityError:
            pass


class Ingreso(Model):
    user = ForeignKeyField(
        User,
        related_name='ingresos',
    )
    timestamp = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=30)
    content = DecimalField(decimal_places=2)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)


class Gasto(Model):
    user = ForeignKeyField(
        User,
        related_name='gastos',
    )
    timestamp = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=30)
    content = DecimalField(decimal_places=2)

    class Meta:
        database = DATABASE
        order_by = ('joined_at',)


class FileContents(Model):
    user = ForeignKeyField(
        User,
        related_name='files',
    )
    name = CharField(max_length=120)
    data = BlobField()

    class Meta:
        database = DATABASE
        order_by = ('joined_at',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Ingreso, Gasto, FileContents], safe=True)
    DATABASE.close()