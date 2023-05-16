# coding:utf8
import time

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType
import pandas as pd
from pyspark.sql import functions as F


if __name__ == '__main__':
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        config("spark.sql.shuffle.partitions", 2).\
        getOrCreate()
    sc = spark.sparkContext

    # 构建一个RDD
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7]).map(lambda x:[x])
    df = rdd.toDF(["num"])

    # TODO 1: 方式1 sparksession.udf.register(), DSL和SQL风格均可以使用
    # UDF的处理函数
    def num_ride_10(num):
        return num * 10
    # 参数1: 注册的UDF的名称, 这个udf名称, 仅可以用于 SQL风格
    # 参数2: UDF的处理逻辑, 是一个单独的方法
    # 参数3: 声明UDF的返回值类型, 注意: UDF注册时候, 必须声明返回值类型, 并且UDF的真实返回值一定要和声明的返回值一致
    # 返回值对象: 这是一个UDF对象, 仅可以用于 DSL 语法
    # 当前这种方式定义的UDF, 可以通过参数1的名称用于SQL风格, 通过返回值对象用户DSL风格
    udf2 = spark.udf.register("udf1", num_ride_10, IntegerType())

    # SQL风格中使用
    # selectExpr 以SELECT的表达式执行, 表达式 SQL风格的表达式(字符串)
    # select方法, 接受普通的字符串字段名, 或者返回值是Column对象的计算
    df.selectExpr("udf1(num)").show()

    # DSL 风格中使用
    # 返回值UDF对象 如果作为方法使用, 传入的参数 一定是Column对象
    df.select(udf2(df['num'])).show()

    # TODO 2: 方式2注册, 仅能用于DSL风格
    udf3 = F.udf(num_ride_10, IntegerType())
    df.select(udf3(df['num'])).show()

    df.selectExpr("udf3(num)").show()
