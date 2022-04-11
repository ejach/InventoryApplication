# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    is_admin = Column(Integer, server_default=text("'0'"))
    is_confirmed = Column(Integer, server_default=text("'0'"))
    phone_num = Column(String(20))


class PartStore(Base):
    __tablename__ = 'part_store'

    id = Column(Integer, primary_key=True)
    part_store_name = Column(String(255), index=True)
    icon = Column(String(255))


class PartType(Base):
    __tablename__ = 'part_type'

    id = Column(Integer, primary_key=True)
    type_name = Column(String(255), index=True)
    type_unit = Column(String(255), index=True)


class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)
    username = Column(String(255))
    time = Column(String(255))
    part_store_name = Column(ForeignKey('part_store.part_store_name', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    parts_used = Column(Integer)

    part_store = relationship('PartStore')


class Part(Base):
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    amount = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    part_number = Column(String(255), index=True, server_default=text("'0'"))
    part_store_name = Column(String(255), index=True)
    low_thresh = Column(Integer)
    type = Column(ForeignKey('part_type.type_name', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    unit = Column(ForeignKey('part_type.type_unit', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    part_type = relationship('PartType', primaryjoin='Part.type == PartType.type_name')
    part_type1 = relationship('PartType', primaryjoin='Part.unit == PartType.type_unit')