# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([('a', 1), ('a', 3)])
    rdd2 = sc.parallelize([('a', 1), ('b', 3)])

    # 通过intersection算子求RDD之间的交集, 将交集取出 返回新RDD
    rdd3 = rdd1.intersection(rdd2)

    print(rdd3.collect())
