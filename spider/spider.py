import requests
from bs4 import BeautifulSoup


base_url = "https://car.autohome.com.cn/"


# 获取车名等基本信息
def get_base_info(soup:BeautifulSoup):
    result = {}
    name = soup.select(".font-bold")[0].string
    result["车名"] = name




    return result

 
# 获取配置信息
def get_config_info(soup:BeautifulSoup,dic:dict):



    return dic
    


if __name__=="__main__":
    for i in range(20):
        url = f"{base_url}price/list-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-{i}.html"
        res = requests.get(url=url)
        content = res.text
        soup = BeautifulSoup(content, "html.parser")
        cars = soup.select(".list-cont")
        cars_info = []
        for car in cars:
            
            car_info = get_base_info(car)

            # 找出配置信息的url
            config_url  = base_url+car.select(".main-lever-link")[0].find_all("a")[-1]["href"]
            res = requests.get(url=url)
            content = res.text
            soup = BeautifulSoup(content, "html.parser")

            car_info = get_config_info(soup,car_info)

            cars_info.append(car_info)
            break
        break

    with open("content.html","w") as f:
        f.write(content)

    


