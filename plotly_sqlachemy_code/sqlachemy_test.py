from sqlalchemy import create_engine,  MetaData, or_, func, and_,Table,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session, scoped_session


engine = create_engine('mysql+pymysql://root:repeatlink@localhost/test', echo=False)
DBsession = sessionmaker(bind=engine)
dbsession = scoped_session(DBsession)   # 线程安全
Base = declarative_base()


class Users(Base):
    __tablename__ = "man"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    country = Column(String(50))

Base.metadata.create_all()













