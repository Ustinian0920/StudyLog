from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_,asc,desc,or_,text,func

from sql_table import User,Admin
engine = create_engine("mysql+pymysql://root:repeatlink@localhost:3306/test",echo=True)
Session = sessionmaker(bind=engine)
session = Session()

user_list = []
for i in range(10):
    user_list.append(User(name=f"{i}lianke",phone=f"{i}12385759",country="China"))
session.add_all(user_list)

admin_list = []
for i in range(5):
    admin_list.append(Admin(name=f"{i}lianke",phone=f"{i}12385759",country="China"))
session.add_all(admin_list)

session.query(User).filter(User.id<6).update({"admin_id":3})
session.query(User).filter(User.id>5).update({"admin_id":4})


session.commit()