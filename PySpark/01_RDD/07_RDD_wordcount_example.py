# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 1. 读取文件获取数据 构建RDD
    file_rdd = sc.textFile("../data/input/words.txt")

    # 2. 通过flatMap API 取出所有的单词
    word_rdd = file_rdd.flatMap(lambda x: x.split(" "))

    # 3. 将单词转换成元组, key是单词, value是1
    word_with_one_rdd = word_rdd.map(lambda word: (word, 1))

    # 4. 用reduceByKey 对单词进行分组并进行value的聚合
    result_rdd = word_with_one_rdd.reduceByKey(lambda a, b: a + b)

    # 5. 通过collect算子, 将rdd的数据收集到Driver中, 打印输出
    print(result_rdd.collect())
