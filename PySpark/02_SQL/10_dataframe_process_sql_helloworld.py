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

    df = spark.read.format("csv").\
        schema("id INT, subject STRING, score INT").\
        load("./PySpark/data/input/sql/stu_score.txt")

    # 注册成临时表
    df.createTempView("score") # 注册临时视图(表)
    df.createOrReplaceTempView("score_2") # 注册 或者 替换  临时视图
    df.createGlobalTempView("score_3") # 注册全局临时视图 全局临时视图在使用的时候 需要在前面带上global_temp. 前缀

    # 可以通过SparkSession对象的sql api来完成sql语句的执行
    spark.sql("SELECT subject, COUNT(*) AS cnt FROM score GROUP BY subject").show()
    spark.sql("SELECT subject, COUNT(*) AS cnt FROM score_2 GROUP BY subject").show()
    spark.sql("SELECT subject, COUNT(*) AS cnt FROM global_temp.score_3 GROUP BY subject").show()
