from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship,backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,ForeignKey

Base = declarative_base()
engine = create_engine("mysql+pymysql://root:repeatlink@localhost:3306/test",echo=True)

# 继承Base基类
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), default=None, nullable=False, comment="用户姓名")
    phone = Column(String(20), default=None, nullable=False, comment="电话")
    country = Column(String(20), default=None, nullable=False, comment="国家")

    # user 指的是 __tablename__
    admin_id = Column(Integer,ForeignKey("admin.id"))

    # 跟数据库无关，不会新增字段，只用于快速链表操作
    # 类名，backref用于反向查询
    admin = relationship("Admin",backref=backref("user",order_by=id))

    # print() 出的结果 相当于toString方法
    def __repr__(self):
        Name = self.name
        Phone = self.phone
        Country = self.country
        return f"User: name: {Name}, phone: {Phone}, country: {Country}"
    
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer,primary_key=True)
    name = Column(String(20), default=None, nullable=False, comment="用户姓名")
    phone = Column(String(20), default=None, nullable=False, comment="电话")
    country = Column(String(20), default=None, nullable=False, comment="国家")

    # print() 出的结果 相当于toString方法
    def __repr__(self):
        Name = self.name
        Phone = self.phone
        Country = self.country
        return f"Admin: name: {Name}, phone: {Phone}, country: {Country}"

if __name__=="__main__":
    # --------表操作
    # 删除表
    Base.metadata.drop_all(engine)
    # 创建表
    Base.metadata.create_all(engine)