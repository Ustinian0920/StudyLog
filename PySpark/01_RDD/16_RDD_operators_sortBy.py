# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('c', 3), ('f', 1), ('b', 11), ('c', 3), ('a', 1), ('c', 5), ('e', 1), ('n', 9), ('a', 1)], 3)

    # 使用sortBy对rdd执行排序

    # 按照value 数字进行排序
    # 参数1函数, 表示的是 ,  告知Spark 按照数据的哪个列进行排序
    # 参数2: True表示升序 False表示降序
    # 参数3: 排序的分区数
    """注意: 如果要全局有序, 排序分区数请设置为1"""
    print(rdd.sortBy(lambda x: x[1], ascending=True, numPartitions=1).collect())

    # 按照key来进行排序
    print(rdd.sortBy(lambda x: x[0], ascending=False, numPartitions=1).collect())
