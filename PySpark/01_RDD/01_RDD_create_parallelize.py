# coding:utf8

# 导入Spark的相关包
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    # 0. 初始化执行环境 构建SparkContext对象
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 演示通过并行化集合的方式去创建RDD, 本地集合 -> 分布式对象(RDD)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # parallelize方法, 没有给定 分区数, 默认分区数是多少?  根据CPU核心来定
    print("默认分区数: ", rdd.getNumPartitions())

    rdd = sc.parallelize([1, 2, 3], 3)
    print("分区数: ", rdd.getNumPartitions())

    # collect方法, 是将RDD(分布式对象)中每个分区的数据, 都发送到Driver中, 形成一个Python List对象
    # collect: 分布式 转 -> 本地集合
    print("rdd的内容是: ", rdd.collect())
