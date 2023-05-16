# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize(["hadoop spark hadoop", "spark hadoop hadoop", "hadoop flink spark"])
    # 得到所有的单词, 组成RDD, flatMap的传入参数 和map一致, 就是给map逻辑用的, 解除嵌套无需逻辑(传参)
    rdd2 = rdd.flatMap(lambda line: line.split(" "))
    print(rdd2.collect())
