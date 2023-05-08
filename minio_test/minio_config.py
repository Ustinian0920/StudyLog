
from minio import Minio
 
# 使用endpoint、access key和secret key来初始化minioClient对象。
minioClient = Minio('192.168.1.191:9000',
                    access_key='pKnctyallbDfVu8c',
                    secret_key='P7g6OiSfAKKEOP4ankNm0311kly6gwPc',
                    secure=False)