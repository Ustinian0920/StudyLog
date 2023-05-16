# coding:utf8
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.storagelevel import StorageLevel
from pyspark.sql.types import StringType

"""
需求1: 各省销售额的统计
需求2: TOP3销售省份中, 有多少店铺达到过日销售额1000+
需求3: TOP3省份中, 各省的平均单单价
需求4: TOP3省份中, 各个省份的支付类型比例

receivable: 订单金额
storeProvince: 店铺省份
dateTS: 订单的销售日期
payType: 支付类型
storeID:店铺ID

2个操作
1. 写出结果到MySQL
2. 写出结果到Hive库
"""


if __name__ == '__main__':
    spark = SparkSession.builder.\
        appName("SparkSQL Example").\
        master("local[*]").\
        config("spark.sql.shuffle.partitions", "2").\
        config("spark.sql.warehouse.dir", "hdfs://node1:8020/user/hive/warehouse").\
        config("hive.metastore.uris", "thrift://node3:9083").\
        enableHiveSupport().\
        getOrCreate()

    # 1. 读取数据
    # 省份信息, 缺失值过滤, 同时省份信息中 会有"null" 字符串
    # 订单的金额, 数据集中有的订单的金额是单笔超过10000的, 这些是测试数据
    # 列值裁剪(SparkSQL会自动做这个优化)
    df = spark.read.format("json").load("../../data/input/mini.json").\
        dropna(thresh=1, subset=['storeProvince']).\
        filter("storeProvince != 'null'").\
        filter("receivable < 10000").\
        select("storeProvince", "storeID", "receivable", "dateTS", "payType")

    # TODO 需求1: 各省 销售额统计
    province_sale_df = df.groupBy("storeProvince").sum("receivable").\
        withColumnRenamed("sum(receivable)", "money").\
        withColumn("money", F.round("money", 2)).\
        orderBy("money", ascending=False)
    province_sale_df.show(truncate=False)

    # 写出MySQL
    province_sale_df.write.mode("overwrite").\
        format("jdbc").\
        option("url", "jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&characterEncoding=utf8").\
        option("dbtable", "province_sale").\
        option("user", "root").\
        option("password", "2212072ok1").\
        option("encoding", "utf-8").\
        save()

    # 写出Hive表 saveAsTable 可以写出表 要求已经配置好Spark On Hive, 配置好后
    # 会将表写入到Hive的数据仓库中
    province_sale_df.write.mode("overwrite").saveAsTable("default.province_sale", "parquet")


    # TODO 需求2: TOP3销售省份中, 有多少店铺达到过日销售额1000+
    # 2.1 先找到TOP3的销售省份
    top3_province_df = province_sale_df.limit(3).select("storeProvince").withColumnRenamed("storeProvince", "top3_province")

    # 2.2 和 原始的DF进行内关联, 数据关联后, 就是全部都是TOP3省份的销售数据了
    top3_province_df_joined = df.join(top3_province_df, on = df['storeProvince'] == top3_province_df['top3_province'])

    top3_province_df_joined.persist(StorageLevel.MEMORY_AND_DISK)
    # 广东省 1 2021-01-03    1005
    # 广东省 2 ....
    # 广东省 3 ....
    # 湖南省 1 ...
    # 湖南省 2 ...
    # 广东省 33
    # 湖南省 123

    # from_unixtime的精度是秒级, 数据的精度是毫秒级, 要对数据进行精度的裁剪
    province_hot_store_count_df = top3_province_df_joined.groupBy("storeProvince", "storeID",
                                    F.from_unixtime(df['dateTS'].substr(0, 10), "yyyy-MM-dd").alias("day")).\
        sum("receivable").withColumnRenamed("sum(receivable)", "money").\
        filter("money > 1000").\
        dropDuplicates(subset=["storeID"]).\
        groupBy("storeProvince").count()

    # 写出MySQL
    province_hot_store_count_df.write.mode("overwrite").\
        format("jdbc").\
        option("url", "jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&characterEncoding=utf8").\
        option("dbtable", "province_hot_store_count").\
        option("user", "root").\
        option("password", "2212072ok1").\
        option("encoding", "utf-8").\
        save()
    # 写出Hive
    province_hot_store_count_df.write.mode("overwrite").saveAsTable("default.province_hot_store_count", "parquet")


    # TODO 需求3: TOP3 省份中 各个省份的平均订单价格(单单价)
    top3_province_order_avg_df = top3_province_df_joined.groupBy("storeProvince").\
        avg("receivable").\
        withColumnRenamed("avg(receivable)", "money").\
        withColumn("money", F.round("money", 2)).\
        orderBy("money", ascending=False)

    top3_province_order_avg_df.show(truncate=False)

    top3_province_order_avg_df.write.mode("overwrite").\
        format("jdbc").\
        option("url", "jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&characterEncoding=utf8").\
        option("dbtable", "top3_province_order_avg").\
        option("user", "root").\
        option("password", "2212072ok1").\
        option("encoding", "utf-8").\
        save()

    top3_province_order_avg_df.write.mode("overwrite").saveAsTable("default.top3_province_order_avg", "parquet")

    # TODO 需求4: TOP3 省份中, 各个省份的支付比例
    # 湖南省 支付宝 33%
    # 湖南省 现金 36%
    # 广东省 微信 33%

    top3_province_df_joined.createTempView("province_pay")

    def udf_func(percent):
        return str(round(percent * 100, 2)) + "%"
    # 注册UDF
    my_udf = F.udf(udf_func, StringType())

    pay_type_df = spark.sql("""
        SELECT storeProvince, payType, (COUNT(payType) / total) AS percent FROM
        (SELECT storeProvince, payType, count(1) OVER(PARTITION BY storeProvince) AS total FROM province_pay) AS sub
        GROUP BY storeProvince, payType, total
    """).withColumn("percent", my_udf("percent"))

    pay_type_df.show()
    pay_type_df.write.mode("overwrite").\
        format("jdbc").\
        option("url", "jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&characterEncoding=utf8").\
        option("dbtable", "pay_type").\
        option("user", "root").\
        option("password", "2212072ok1").\
        option("encoding", "utf-8").\
        save()

    pay_type_df.write.mode("overwrite").saveAsTable("default.pay_type", "parquet")

    top3_province_df_joined.unpersist()
