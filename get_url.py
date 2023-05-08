import json
import requests
import base64
from Crypto.Cipher import AES

login_url = "http://192.168.6.1:6080/login/loginAuth.action"
vncs_url = "http://192.168.6.1:6080/desktopandapp/api/vncs"
ips_url = "http://192.168.6.1:6080/desktopandapp/api/ips"

class EncryptDate:
    def __init__(self, key):
        self.key = key                              # 初始化密钥
        self.length = 16                            # 初始化数据块大小
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        self.unpad = lambda date: date[0:-ord(date[-1])]  # 截断函数，去除填充的字符

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数
        a = self.pad(encrData)
        res = self.aes.encrypt(a.encode("utf-8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf-8"))
        msg = self.aes.decrypt(res).decode("utf-8")
        return self.unpad(msg)

# 获取cookies
def get_cookies(username,password):
    global login_url
    data = {"strUserName": username,
            "strPassword": password,
            "strUserType": "os",
            "authCode":""
            }

    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
            }

    res = requests.post(url=login_url,data=data)#,headers=headers
    print(res.text)
    code = res.status_code
    print("获取cookies状态码:",code)
    cookies = res.cookies
    return cookies

# 获取VNC
def get_vncs(cookies):
    global vncs_url 
    aes_key = "SugonGridview123"

    params = {"limit":"2147483647",
            "sort":"DESC",
            "start":"0",
            "orderBy":"jobs"
            }

    res = requests.get(url=vncs_url,params=params, cookies=cookies)
    print(res.text)
    print("获取vncs状态码:",res.status_code)
    result = res.text.encode("utf8")
    result = json.loads(result)

    for i,data in enumerate(result["data"]["datalist"]):
        aes_text = data["passwd"]
        print("加密前:",aes_text)
        eg = EncryptDate(aes_key.encode("utf-8"))
        encrypt_passwd = eg.encrypt(aes_text)
        result["data"]["datalist"][i]["passwd"] = encrypt_passwd

    data = result["data"]["datalist"]
    
    return data
 

def vncsession():
    url = "http://192.168.6.1:6080/desktopandapp/api/vncs/vncsession"
    res = requests.post(url=url,cookies=cookies)
    print(res.text)

# 获取IP
def get_ips(cookies):
    global ips_url
    params = {"hostName":"login1"}
    res = requests.get(url=ips_url,params=params, cookies=cookies)
    print(res.text)
    result = res.text.encode("utf8")
    result = json.loads(result)
    code = result["code"]
    print("获取ips状态码:",res.status_code)
    ips = result["data"]
    return (code,ips)



# 获取novncUrl
def get_novnc_url(cookies,sid,vnchost,vncip,passwd,vncuser):
    
    url = f"http://192.168.6.1:6080/desktopandapp/api/vncs/hostname/{vnchost}/{sid}/action/launchNoVnc"

    params = {"sid":sid,
            "vnchost":vnchost,
            "vncip":vncip,
            "vncpasswd":passwd,
            "vncuser":vncuser}

    res = requests.get(url=url,params=params, cookies=cookies)
    result = res.text.encode("utf8")
    result = json.loads(result)
    print(result)
    novncUrl =  result["data"]["novncUrl"]
    print("获取novncUrl状态码:",res.status_code)
    return novncUrl

if __name__=="__main__":

    url = "http://192.168.6.1:6080/login/checkLock.action"
    res = requests.post(url=url)
    result = res.text.encode("utf8")
    result = json.loads(result)
    print(type(result["result"]))


    username = "lianke"
    password = "lk123Aa"
    cookies = get_cookies(username,password)
    vncs = get_vncs(cookies)
    get_ips(cookies)
    print("vncs:",vncs)
    if vncs==[]:
        vncsession()
        vncs = get_vncs(cookies)
    data = vncs[0]
    sid = data["sid"]
    vnchost = data["hostname"]
    vncip = data["ip"]
    vncpasswd = data["passwd"]
    vncuser = data["user"]

    novnc_url = get_novnc_url(cookies,sid,vnchost,vncip,vncpasswd,vncuser)
    print(novnc_url)



