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

    # JSON类型自带有Schema信息
    df = spark.read.format("json").load("./PySpark/data/input/sql/people.json") 
    df.printSchema() 
    df.show()
 