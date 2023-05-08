# coding: utf-8
from sqlalchemy import *
from sqlalchemy.orm import declarative_base,sessionmaker

import datetime

now_time = datetime.datetime.now().strftime('%Y-%m-%d')

Base  =  declarative_base()  #生成orm基类
engine = create_engine('mysql+pymysql://app:repeatlink@192.168.1.191:3306/xq_plus', echo=False)
session = sessionmaker(bind=engine)()



result = session.execute("select * from defect_dangerous_point")
for item in result:
    print(item)

session.execute(f"delete from defect_dangerous_point where id=9 ")

session.commit()
session.close()





