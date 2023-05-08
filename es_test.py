from elasticsearch import Elasticsearch
 
 
class ElasticSearchClass(object):

    def __init__(self, host, port, user, passwrod):
      
        http_auth = user + ":" + passwrod 
        self.es = Elasticsearch(
            [host],
            port=port,
            http_auth=http_auth,
            # sniff_on_start=True,  # 启动前嗅探es集群服务器
            sniff_on_connection_fail=True,  # es集群服务器节点连接异常时是否刷新es节点信息
            sniff_timeout=60  # 每60秒刷新节点信息
        )

    # 创建索引
    # @retry(tries=3)
    def create_index(self, index_name, mapping):
 
        self.es.indices.create(index=index_name, ignore=400)
        self.es.indices.put_mapping(index=index_name, body=mapping)

    # 插入一条数据
    def insert(self, index, type, body, id=None):
        '''
        插入一条body给指定的index、指定的type下;
        可指定Id,若不指定,ES会自动生成
        :param index: 待插入的index值      
        :param body: 待插入的数据  # dict型
        :param id: 自定义Id值
        :return:
        '''
        return self.es.index(index=index,doc_type=type,body=body,id=id,request_timeout=30)
    
    # 查询一条数据
    def get(self, doc_type, indexname, id):
        # index中具体的一条
        return self.es.get(index=indexname,doc_type=doc_type, id=id)
    
    #通过index搜索数据  其中，搜索之后数据显示默认为十条数据
    def searchindex(self, index):
        """
        查找所有index数据
        """
        try:
            return self.es.search(index=index)
        except Exception as err:
            print(err)

    # 查找index下所有符合条件的数据
    def searchDoc(self, index=None, type=None, body=None):
        '''
        查找index下所有符合条件的数据
        :param index:
        :param type:
        :param body: 筛选语句,符合DSL语法格式
        :return:
        '''
        return self.es.search(index=index, doc_type=type, body=body)

    # 更新其中具体的一条
    def update(self, doc_type, indexname,  body, data, id):
        # 更新其中具体的一条
        return self.es.update(index=indexname,doc_type=doc_type,  body=body, data=data, id=id)
    


es = Elasticsearch("http://192.168.1.175:30105")

result = es.info()



print(result)





