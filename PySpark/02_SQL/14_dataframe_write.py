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

    # 1. 读取数据集
    schema = StructType().add("user_id", StringType(), nullable=True). \
        add("movie_id", IntegerType(), nullable=True). \
        add("rank", IntegerType(), nullable=True). \
        add("ts", StringType(), nullable=True)
    df = spark.read.format("csv"). \
        option("sep", "\t"). \
        option("header", False). \
        option("encoding", "utf-8"). \
        schema(schema=schema). \
        load("../data/input/sql/u.data")

    # Write text 写出, 只能写出一个列的数据, 需要将df转换为单列df
    df.select(F.concat_ws("---", "user_id", "movie_id", "rank", "ts")).\
        write.\
        mode("overwrite").\
        format("text").\
        save("../data/output/sql/text")

    # Write csv
    df.write.mode("overwrite").\
        format("csv").\
        option("sep", ";").\
        option("header", True).\
        save("../data/output/sql/csv")

    # Write json
    df.write.mode("overwrite").\
        format("json").\
        save("../data/output/sql/json")

    # Write parquet
    df.write.mode("overwrite").\
        format("parquet").\
        save("../data/output/sql/parquet")


