import requests
from lxml import etree 
import time
import json
import os

class AgentPool:
    """
    # 实例化对象 
    ap = AgentPool
    # 运行代理池,爬取5页
    ap.run(5)
    # 检测代理池IP可用性，去掉不可用IP
    ap.flush()
    # 获取IP列表
    ip_list = ap.get()
    """

    def __init__(self) -> None:
        self.json_path = os.path.abspath(os.path.dirname(__file__))+"/ip_pool.json"

    # 1.发送请求，获取响应
    def send_request(self,page):
        print("=============正在抓取第{}页===========".format(page))
        # 目标网页，添加headers参数
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',"Connection":"close"}

        # 发送请求：模拟浏览器发送请求，获取响应数据
        response = requests.get(base_url,headers=headers)
        data = response.content.decode()
        time.sleep(1)

        return data

    # 2.解析数据
    def parse_data(self,data):
        
        # 数据转换
        html_data =  etree.HTML(data)
        # 分组数据
        parse_list = html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
    
        return parse_list

    # 4.检测代理IP
    def check_ip(self,proxies_list):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',"Connection":"close"}

        can_use = []
        for i,proxies in enumerate(proxies_list):
            try:
                print(f"正在验证第{i}个ip")
                response = requests.get('https://www.baidu.com/',headers=headers,proxies=proxies,timeout=0.1)
                if response.status_code == 200:
                    can_use.append({"ip":proxies})

            except Exception as e:
                print(e)
                
        return {"data":can_use}

    # 5.保存到文件
    def save(self,can_use):
        
        with open(self.json_path,"w") as f:
            json.dump(can_use,f)
    
    # 实现主要逻辑
    def run(self,page):
        proxies_list = []
        # 实现翻页
        for page in range(1,page):
            data = self.send_request(page)
            parse_list = self.parse_data(data)
            # 3.获取数据
            for i,tr in enumerate(parse_list):
                print(f"正在解析第{i}条")
                proxies_dict  = {}
                http_type = tr.xpath('./td[4]/text()')
                ip_num = tr.xpath('./td[1]/text()')
                port_num = tr.xpath('./td[2]/text()')

                http_type = ' '.join(http_type)
                ip_num = ' '.join(ip_num)
                port_num = ' '.join(port_num)

                proxies_dict[http_type] = ip_num + ":" + port_num

                proxies_list.append(proxies_dict)
        
        print("获取到的代理IP数量：",len(proxies_list))

        can_use = self.check_ip(proxies_list)

        print("能用的代理IP数量：",len(can_use)) 
        print("能用的代理IP:",can_use) 

        self.save(can_use)

    # 获取ip列表
    def get(self):
        ip_list = []
        with open(self.json_path,"r") as f:
            dic = json.load(f)
            for ip in dic.get("data"):
                ip_list.append(ip.get("ip").get("HTTP"))
        return ip_list

    # 检测代理池IP可用性，去掉不可用IP
    def flush(self):
        ip_list = self.get()
        can_use = self.check_ip(ip_list)
        self.save(can_use)

if __name__ == "__main__": 
    ap = AgentPool()
    ap.run(5)
    print(ap.get())
    