import os
 
replace_mapper = {
    "from flask_sqlalchemy import SQLAlchemy":"from sqlalchemy import *\nfrom sqlalchemy.orm import sessionmaker,declarative_base",
    "db = SQLAlchemy()":"Base  =  declarative_base()  #生成orm基类\nengine = create_engine('mysql+pymysql://app:repeatlink@192.168.1.191:3306/xq_plus', echo=False)\nsession = sessionmaker(bind=engine)"
}

# "mysql+pymysql://app:repeatlink@192.168.1.191:3306/xq_plus"
def create_models():
    db_url = "mysql+pymysql://root:repeatlink@localhost:3306/test"
    project_path = os.getcwd()
    print(project_path)
    model_path = os.path.join(project_path, 'models.py')
    cmd = 'flask-sqlacodegen --flask {}'.format(db_url)
    try:
        output = os.popen(cmd)
        print(f"output:{output}")
        resp = output.buffer.read().decode(encoding='utf-8')
        content = str(resp)
        for k,v in replace_mapper.items():
            content = content.replace(k,v)
        output.close()
        # w+ 读写权限
        with open(model_path, 'w+', encoding='utf-8') as f:
            f.write(content)
        print('create models successfully!')
    except Exception as e:
        print(e)
 
 
if __name__ == '__main__':
    create_models()