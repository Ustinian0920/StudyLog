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

    # 读取CSV文件
    df = spark.read.format("csv").\
        option("sep", ";").\
        option("header", True).\
        option("encoding", "utf-8").\
        schema("name STRING, age INT, job STRING").\
        load("../data/input/sql/people.csv")

    df.printSchema()
    df.show()
