# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.textFile("../data/input/words.txt")
    rdd2 = rdd.flatMap(lambda x: x.split(" ")).map(lambda x: (x, 1))

    # 通过countByKey来对key进行计数, 这是一个Action算子
    result = rdd2.countByKey()

    print(result)
    print(type(result))
