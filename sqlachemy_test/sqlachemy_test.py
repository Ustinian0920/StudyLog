from sqlalchemy import create_engine,  MetaData, or_, func, and_,Table,Column,Integer,String

from sqlalchemy.orm import sessionmaker,declarative_base
 

Base  =  declarative_base()  #生成orm基类
engine = create_engine('mysql+pymysql://root:repeatlink@localhost/test', echo=False)
session = sessionmaker(bind=engine)



class Users(Base):
    __tablename__ = "man"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    country = Column(String(50))















