# coding:utf8

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([ (1001, "zhangsan"), (1002, "lisi"), (1003, "wangwu"), (1004, "zhaoliu") ])
    rdd2 = sc.parallelize([ (1001, "销售部"), (1002, "科技部")])

    # 通过join算子来进行rdd之间的关联
    # 对于join算子来说 关联条件 按照二元元组的key来进行关联
    print(rdd1.join(rdd2).collect())

    # 左外连接, 右外连接 可以更换一下rdd的顺序 或者调用rightOuterJoin即可
    print(rdd1.leftOuterJoin(rdd2).collect())
