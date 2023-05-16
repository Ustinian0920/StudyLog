# coding:utf8

# 导入Spark的相关包
import time

from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel
from defs import context_jieba, filter_words, append_words, extract_user_and_word
from operator import add

if __name__ == '__main__':
    # 0. 初始化执行环境 构建SparkContext对象
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # 1. 读取数据文件
    file_rdd = sc.textFile("hdfs://node1:8020/input/SogouQ.txt")

    # 2. 对数据进行切分 \t
    split_rdd = file_rdd.map(lambda x: x.split("\t"))

    # 3. 因为要做多个需求, split_rdd 作为基础的rdd 会被多次使用.
    split_rdd.persist(StorageLevel.DISK_ONLY)

    # TODO: 需求1: 用户搜索的关键`词`分析
    # 主要分析热点词
    # 将所有的搜索内容取出
    # print(split_rdd.takeSample(True, 3))
    context_rdd = split_rdd.map(lambda x: x[2])

    # 对搜索的内容进行分词分析
    words_rdd = context_rdd.flatMap(context_jieba)

    # print(words_rdd.collect())
    # 院校 帮 -> 院校帮
    # 博学 谷 -> 博学谷
    # 传智播 客 -> 传智播客
    filtered_rdd = words_rdd.filter(filter_words)
    # 将关键词转换: 穿直播 -> 传智播客
    final_words_rdd = filtered_rdd.map(append_words)
    # 对单词进行 分组 聚合 排序 求出前5名
    result1 = final_words_rdd.reduceByKey(lambda a, b: a + b).\
        sortBy(lambda x: x[1], ascending=False, numPartitions=1).\
        take(5)

    print("需求1结果: ", result1)

    # TODO: 需求2: 用户和关键词组合分析
    # 1, 我喜欢传智播客
    # 1+我  1+喜欢 1+传智播客
    user_content_rdd = split_rdd.map(lambda x: (x[1], x[2]))
    # 对用户的搜索内容进行分词, 分词后和用户ID再次组合
    user_word_with_one_rdd = user_content_rdd.flatMap(extract_user_and_word)
    # 对内容进行 分组 聚合 排序 求前5
    result2 = user_word_with_one_rdd.reduceByKey(lambda a, b: a + b).\
        sortBy(lambda x: x[1], ascending=False, numPartitions=1).\
        take(5)

    print("需求2结果: ", result2)

    # TODO: 需求3: 热门搜索时间段分析
    # 取出来所有的时间
    time_rdd = split_rdd.map(lambda x: x[0])
    # 对时间进行处理, 只保留小时精度即可
    hour_with_one_rdd = time_rdd.map(lambda x: (x.split(":")[0], 1))
    # 分组 聚合 排序
    result3 = hour_with_one_rdd.reduceByKey(add).\
        sortBy(lambda x: x[1], ascending=False, numPartitions=1).\
        collect()

    print("需求3结果: ", result3)

    time.sleep(100000)
