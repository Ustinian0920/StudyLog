# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 读取小文件文件夹
    rdd= sc.wholeTextFiles("./PySpark/data/input/tiny_files")
    print(rdd.map(lambda x:x[1]).collect())
