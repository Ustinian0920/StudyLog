from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_,asc,desc,or_,text,func

from sql_table import User
engine = create_engine("mysql+pymysql://root:repeatlink@localhost:3306/test",echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# 创建实例
NewUser = User(name=f"lianke", phone=f"18102374658", country="China")

# 批量创建实例并更新
account_all = [User(name="lk",phone="12309765",country="China"),User(name="repeatlink",phone="12132309765",country="China")]
# session.add_all(account_all)


# # 增加实例
# session.add(NewUser)
# # 删除实例
# session.delete(NewUser)
# # 修改实例
# session.merge(NewUser)

# 查询实例
results = session.query(User).filter(User.country=='China')
for result in results:
    print(f"查询结果为: {result}")

# 先查询字段，再对其更新
result = session.query(User).filter(User.name=="repeatlink").first()
result.name = "repeatlink"
session.add(result)

# 先查询字段，再对其删除
# result = session.query(User).filter(User.name=="repeatlink").delete()

# 先查询字段，再对其删除
result = session.query(User).filter_by(name="repeatlink").update({"name":"repeatlink"})

# :value 和 :name 是占位符  desc降序
result = session.query(User).filter(text("id<:value and name=:name")).params(value=4, name='repeatlink').order_by(User.id.desc()).all()

# and
results = session.query(User).filter( and_(User.phone=="0",User.id<9) )
for result in results:
    print(f"查询结果为{result}")

# in 
results = session.query(User).filter( User.name.in_(["0lianke","1lianke"]) )
for result in results:
    print(f"查询结果为{result}")




#分组之后取最大id，id之和，最小id
ret = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.country).all()

#haviing筛选
ret = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.name).having(func.min(User.id) >2).all()


session.commit()	# 需要调用commit()方法提交事务。


