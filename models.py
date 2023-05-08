# coding: utf-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,declarative_base


Base  =  declarative_base()  #生成orm基类
engine = create_engine('mysql+pymysql://app:repeatlink@192.168.1.191:3306/xq_plus', echo=False)
session = sessionmaker(bind=engine)



class ExprimentDatum(db.Model):
    __tablename__ = 'ExprimentData'

    id = db.Column(db.Integer, primary_key=True)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    data = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    update_user_id = db.Column(db.Integer)



class PrivateFlow(db.Model):
    __tablename__ = 'PrivateFlow'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    struct = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    create_time = db.Column(db.Time)
    describ = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    public_id = db.Column(db.Integer, info='拷贝的公共卡片的id')
    language = db.Column(db.String(50), info='开发语言\\n')
    author = db.Column(db.String(50))
    name = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))



class PrivateSub(db.Model):
    __tablename__ = 'PrivateSub'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    describ = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    create_time = db.Column(db.Time)
    user_id = db.Column(db.Integer)
    public_id = db.Column(db.Integer, info='拷贝的公共卡片的id')
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))



class PublicFlow(db.Model):
    __tablename__ = 'PublicFlow'

    id = db.Column(db.Integer, primary_key=True)
    struct = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    create_time = db.Column(db.Time)
    update_user_id = db.Column(db.Integer)
    describ = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    name = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))



class PublicSub(db.Model):
    __tablename__ = 'PublicSub'

    id = db.Column(db.Integer, primary_key=True)
    update_user_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    describ = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    parameters = db.Column(db.JSON)
    update_time = db.Column(db.Time)
    create_time = db.Column(db.Time)
    language = db.Column(db.String(50))
    author = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    department = db.Column(db.String(50))
    program = db.Column(db.String(50))
    output = db.Column(db.String(50))



class ShotInfo(db.Model):
    __tablename__ = 'ShotInfo'

    id = db.Column(db.Integer, primary_key=True)
    shot = db.Column(db.Integer)
    is_follow = db.Column(db.Integer)



class TimeInfo(db.Model):
    __tablename__ = 'TimeInfo'

    id = db.Column(db.Integer, primary_key=True)
    shot_info_id = db.Column(db.Integer)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    R = db.Column(db.LargeBinary)
    Z = db.Column(db.LargeBinary)
    P = db.Column(db.LargeBinary)
    X = db.Column(db.LargeBinary)
    y1 = db.Column(db.LargeBinary)
    y2 = db.Column(db.LargeBinary)
    y3 = db.Column(db.LargeBinary)
    y4 = db.Column(db.LargeBinary)
    y5 = db.Column(db.LargeBinary)
    p1 = db.Column(db.Float)
    p2 = db.Column(db.Float)
    p3 = db.Column(db.Float)
    p4 = db.Column(db.Float)
    p5 = db.Column(db.Float)
    p6 = db.Column(db.Float)
    p7 = db.Column(db.Float)
    p8 = db.Column(db.Float)
    p9 = db.Column(db.Float)



class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.Integer, info='管理员权限 0普通用户 1管理员')



class UserDatum(db.Model):
    __tablename__ = 'UserData'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    data = db.Column(db.JSON)
    update_time = db.Column(db.Time)
