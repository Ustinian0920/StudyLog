# coding:utf8

# SparkSession对象的导包, 对象是来自于 pyspark.sql包中
from pyspark.sql import SparkSession

if __name__ == '__main__':
    # 构建SparkSession执行环境入口对象
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        getOrCreate()

    # 通过SparkSession对象 获取 SparkContext对象
    sc = spark.sparkContext

    # SparkSQL的HelloWorld
    df = spark.read.csv("../data/input/stu_score.txt", sep=',', header=False)
    df2 = df.toDF("id", "name", "score")
    df2.printSchema()
    df2.show()

    df2.createTempView("score")

    # SQL 风格
    spark.sql("""
        SELECT * FROM score WHERE name='语文' LIMIT 5
    """).show()

    # DSL 风格
    df2.where("name='语文'").limit(5).show()
