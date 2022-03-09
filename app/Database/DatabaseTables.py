# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


# Accounts database
class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    is_admin = Column(Integer, server_default=text("'0'"))
    is_confirmed = Column(Integer, server_default=text("'0'"))


# Vans database
class Van(Base):
    __tablename__ = 'vans'

    id = Column(Integer, primary_key=True)
    van_number = Column(String(255), index=True)


# Jobs database
class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)
    username = Column(String(255))
    time = Column(String(255))
    van_number = Column(ForeignKey('vans.van_number', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    parts_used = Column(Integer)

    van = relationship('Van')


# Parts database
class Part(Base):
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    amount = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    part_number = Column(String(255), index=True, server_default=text("'0'"))
    van_number = Column(ForeignKey('vans.van_number', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    low_thresh = Column(Integer)

    van = relationship('Van')
