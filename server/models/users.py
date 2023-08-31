from config.db import meta
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String


users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('username', String(255)),
    Column('email', String(255)),
    Column('password', String(255))
)