# coding:utf8

from pyspark import SparkConf, SparkContext
from defs_19 import city_with_category
import json
import os
os.environ['HADOOP_CONF_DIR'] = "/export/server/hadoop/etc/hadoop"

if __name__ == '__main__':
    # 提交 到yarn集群, master 设置为yarn
    conf = SparkConf().setAppName("test-yarn-1").setMaster("yarn")
    # 如果提交到集群运行, 除了主代码以外, 还依赖了其它的代码文件
    # 需要设置一个参数, 来告知spark ,还有依赖文件要同步上传到集群中
    # 参数叫做: spark.submit.pyFiles
    # 参数的值可以是 单个.py文件,   也可以是.zip压缩包(有多个依赖文件的时候可以用zip压缩后上传)
    conf.set("spark.submit.pyFiles", "defs_19.py")
    sc = SparkContext(conf=conf)

    # 在集群中运行, 我们需要用HDFS路径了. 不能用本地路径
    file_rdd = sc.textFile("hdfs://node1:8020/input/order.text")

    # 进行rdd数据的split 按照|符号进行, 得到一个个的json数据
    jsons_rdd = file_rdd.flatMap(lambda line: line.split("|"))

    # 通过Python 内置的json库, 完成json字符串到字典对象的转换
    dict_rdd = jsons_rdd.map(lambda json_str: json.loads(json_str))

    # 过滤数据, 只保留北京的数据
    beijing_rdd = dict_rdd.filter(lambda d: d['areaName'] == "北京")

    # 组合北京 和 商品类型形成新的字符串
    category_rdd = beijing_rdd.map(city_with_category)

    # 对结果集进行去重操作
    result_rdd = category_rdd.distinct()

    # 输出
    print(result_rdd.collect())
