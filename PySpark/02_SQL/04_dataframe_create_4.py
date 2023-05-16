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

    # 基于Pandas的DataFrame构建SparkSQL的DataFrame对象
    pdf = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["张大仙", "王晓晓", "吕不为"],
            "age": [11, 21, 11]
        }
    )

    df = spark.createDataFrame(pdf)

    df.printSchema()
    df.show()
