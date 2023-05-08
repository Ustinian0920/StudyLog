from minio_bucket import Bucket
from minio_object import Object
from minio_presigned import Presigned


if __name__=="__main__":
    bkt = Bucket()

    bkt_list = bkt.get_bucket_list()
    print(f'bkt_list:{bkt_list}')
    # bkt_obj_list = bkt.get_bucket_files()
    # print(f"obj_list:{bkt_obj_list}")