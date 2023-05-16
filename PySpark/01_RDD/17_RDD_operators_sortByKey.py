# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('a', 1), ('E', 1), ('C', 1), ('D', 1), ('b', 1), ('g', 1), ('f', 1),
                          ('y', 1), ('u', 1), ('i', 1), ('o', 1), ('p', 1),
                          ('m', 1), ('n', 1), ('j', 1), ('k', 1), ('l', 1)], 3)

    print(rdd.sortByKey(ascending=True, numPartitions=1, keyfunc=lambda key: str(key).lower()).collect())
