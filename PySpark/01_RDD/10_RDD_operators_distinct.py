# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 1, 1, 2, 2, 2, 3, 3, 3])

    # distinct 进行RDD数据去重操作
    print(rdd.distinct().collect())

    rdd2 = sc.parallelize([('a', 1), ('a', 1), ('a', 3)])
    print(rdd2.distinct().collect())
