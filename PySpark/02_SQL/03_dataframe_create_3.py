# coding:utf8

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType


if __name__ == '__main__':
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        getOrCreate()
    sc = spark.sparkContext

    # 基于RDD转换成DataFrame
    rdd = sc.textFile("./PySpark/data/input/sql/people.txt").\
        map(lambda x: x.split(",")).\
        map(lambda x: (x[0], int(x[1])))


    # toDF的方式构建DataFrame
    df1 = rdd.toDF(["name", "age"])
    df1.printSchema()
    df1.show()

    # toDF的方式2 通过StructType来构建
    schema = StructType().add("name", StringType(), nullable=True).\
        add("age", IntegerType(), nullable=False)

    df2 = rdd.toDF(schema=schema)
    df2.printSchema()
    df2.show()
