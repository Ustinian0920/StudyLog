# coding:utf8
import string
import time

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType, ArrayType
import pandas as pd
from pyspark.sql import functions as F


if __name__ == '__main__':
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        config("spark.sql.shuffle.partitions", 2).\
        config("spark.sql.warehouse.dir", "hdfs://node1:8020/user/hive/warehouse").\
        config("hive.metastore.uris", "thrift://node3:9083").\
        enableHiveSupport().\
        getOrCreate()
    sc = spark.sparkContext

    spark.sql("SELECT * FROM student").show()


