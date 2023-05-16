# coding:utf8

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType
import pandas as pd


if __name__ == '__main__':
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        getOrCreate()
    sc = spark.sparkContext

    # 读取parquet类型的文件
    df = spark.read.format("parquet").load("./PySpark/data/input/sql/users.parquet")

    df.printSchema()
    df.show()
