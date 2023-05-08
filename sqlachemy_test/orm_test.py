# coding: utf-8
from sqlalchemy import *
from sqlalchemy.orm import declarative_base,sessionmaker

import datetime

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

Base  =  declarative_base()  #生成orm基类
engine = create_engine('mysql+pymysql://root:repeatlink@localhost:3306/test', echo=False)
session = sessionmaker(bind=engine)()




class TimeInfo(db.Model):
    __tablename__ = 'TimeInfo'

    id = db.Column(db.Integer, primary_key=True)
    shot_info_id = db.Column(db.Integer)
    shot = db.Column(db.Integer)
    time = db.Column(db.Integer)
    R = db.Column(db.LargeBinary)
    Z = db.Column(db.LargeBinary)
    P = db.Column(db.LargeBinary)
    X = db.Column(db.Text)
    y1 = db.Column(db.Text)
    y2 = db.Column(db.Text)
    y3 = db.Column(db.Text)
    y4 = db.Column(db.Text)
    y5 = db.Column(db.Text)
    p1 = db.Column(db.Float)
    p2 = db.Column(db.Float)
    p3 = db.Column(db.Float)
    p4 = db.Column(db.Float)
    p5 = db.Column(db.Float)
    p6 = db.Column(db.Float)
    p7 = db.Column(db.Float)
    p8 = db.Column(db.Float)
    p9 = db.Column(db.Float)


# 增
for i in range(3,10):
    ddp = DefectDangerousPoint(
                            id = i,
                            defect_id = i,
                            defect_detail_id = i,
                            point = "1.机械伤害，2.顶盖内潮湿，防止滑倒",
                            sort_code = 0,
                            source = 1,
                            status = 0,
                            create_user_id = f"user{i}",
                            create_time = now_time,
                            update_user_id = f"user{i}",
                            update_time = now_time
                            )
    session.add(ddp)



# 删
# 删除id为4的
session.query(DefectDangerousPoint).filter(DefectDangerousPoint.id == 4).delete()

# 改
# 改id为2的 point 为 "修改后的值"
update_dic = {"point":"修改后的值"}
session.query(DefectDangerousPoint).filter(DefectDangerousPoint.defect_id==2).update(update_dic)


# 查
# 查询status为0的数据
ddps = session.query(DefectDangerousPoint).filter(DefectDangerousPoint.status==0).all()

for ddp in ddps:
    print(f"查询结果为{ddp}")



session.commit()

session.close()