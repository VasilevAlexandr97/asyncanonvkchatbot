from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData()

user = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('vkid', BigInteger, nullable=False),
    Column('name', String(100), nullable=True),
    Column('state', String(32), nullable=True),
    Column('room', Integer, nullable=True),
    Column('sex', String(8), nullable=False),
    Column('count_rep', Float, default=0),
    Column('full_rep', Float, default=0),
    Column('reputation', Float, default=0),
    Column('age', String(8), nullable=True),
    Column('find_sex', String(8), nullable=True),
)


room = Table(
    'rooms', meta,
    Column('id', Integer, primary_key=True),
    Column('f_user', BigInteger, nullable=False),
    Column('s_user', BigInteger, nullable=True),
    Column('first_message_time', DateTime),
    Column('last_message_time', DateTime),
    Column('sex', String(8)),
    Column('reputation', Float, default=0),
    Column('find_sex', String(8), nullable=True),
    Column('find_age', String(8), nullable=True)
)