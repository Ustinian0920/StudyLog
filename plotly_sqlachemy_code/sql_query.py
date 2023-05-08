from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_,asc,desc,or_,text,func

from sql_table import User,Admin
engine = create_engine("mysql+pymysql://root:repeatlink@localhost:3306/test",echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# .all() 可以把sqlalchemy.orm.query.Query类型 转为 list类型
results = session.query(User).filter( User.name.in_(["0lianke","1lianke"]) ).all()


#分组之后取最大id，id之和，最小id
results = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.country).all()

for result in results:
    print(f"查询结果为{result}")


#haviing筛选
results = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.country).having(func.max(User.id) >3).all()

for result in results:
    print(f"查询结果为{result}")

# relationship 正向查询
u = session.query(User).first()
print(u.admin.name)

# relationship 反向查询
a = session.query(Admin).filter_by(id=3).first()
print(a.user)



session.commit()	# 需要调用commit()方法提交事务。