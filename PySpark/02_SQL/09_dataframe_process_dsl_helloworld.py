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

    # Column对象的获取
    id_column = df['id']
    subject_column = df['subject']

    # DLS风格演示
    df.select(["id", "subject"]).show()
    df.select("id", "subject").show()
    df.select(id_column, subject_column).show()

    # filter API
    df.filter("score < 99").show()
    df.filter(df['score'] < 96).show()

    # where API
    df.where("score < 99").show()
    df.where(df['score'] < 99).show()

    # group By API
    df.groupBy("subject").count().show()
    df.groupBy(df['subject']).count().show()


    # df.groupBy API的返回值 GroupedData
    # GroupedData对象 不是DataFrame
    # 它是一个 有分组关系的数据结构, 有一些API供我们对分组做聚合
    # SQL: group by 后接上聚合: sum avg count min man
    # GroupedData 类似于SQL分组后的数据结构, 同样有上述5种聚合方法
    # GroupedData 调用聚合方法后, 返回值依旧是DataFrame
    # GroupedData 只是一个中转的对象, 最终还是要获得DataFrame的结果
    r = df.groupBy("subject")
