# coding:utf8

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType
import pandas as pd
from pyspark.sql import functions as F


if __name__ == '__main__':
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        getOrCreate()
    sc = spark.sparkContext

    # TODO 1: SQL 风格进行处理
    rdd = sc.textFile("../data/input/words.txt").\
        flatMap(lambda x: x.split(" ")).\
        map(lambda x: [x])

    df = rdd.toDF(["word"])

    # 注册DF为表格
    df.createTempView("words")

    spark.sql("SELECT word, COUNT(*) AS cnt FROM words GROUP BY word ORDER BY cnt DESC").show()


    # TODO 2: DSL 风格处理
    df = spark.read.format("text").load("../data/input/words.txt")

    # withColumn方法
    # 方法功能: 对已存在的列进行操作, 返回一个新的列, 如果名字和老列相同, 那么替换, 否则作为新列存在
    df2 = df.withColumn("value", F.explode(F.split(df['value'], " ")))
    df2.groupBy("value").\
        count().\
        withColumnRenamed("value", "word").\
        withColumnRenamed("count", "cnt").\
        orderBy("cnt", ascending=False).\
        show()
