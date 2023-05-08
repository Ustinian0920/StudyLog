from apps.common_model import SysDict
from apps.defect_lib.model import MstTag
from exts import db
# 用户可选择的标签
Labels = [
    {
        "major": "机械",
        "groups": ["水轮机及圆筒阀", "发电机(柴油发电机)", "辅助设备", "大坝机械（含尼日河引水工程）、厂房起重设备、电梯"],
    },
    {
        "major": "一次",
        "groups": [
            "GIS、高压电缆、出线设备、电抗器",
            "发电机（含局放在线监测系统）、20kV设备、15.75kV设备、主变压器",
            "10kV、 6kV、 400V厂用电及照明",
            "通风、空调系统",
        ],
    },
    {
        "major": "保护",
        "groups": [
            "500kV线路、T区、断路器保护、 500kV电抗器保护、500kV电缆保护",
            "安控、母差、同步相量装置、故障录波、保护信息管理系统、电能量采集系统",
            "元件保护、故障测距装置",
        ],
    },
    {
        "major": "监控",
        "groups": [
            "监控上位机系统、监控现地LCU系统",
            "微机五防（含五防网络系统、智能钥匙、智能安柜）、ON-CALL系统、仿真系统、状态分析系统、智能巡检系统（含点检系统）、综合数据平台",
            "工业电视、门禁系统、消防监控系统、安防系统、安风系统（含定位系统）、泄洪报警系统、厂房广播系统",
            "220V交直流系统、UPS系统、通讯系统（含无线WIFI网络）、GPS对时系统",
        ],
    },
    {
        "major": "自动",
        "groups": [
            "主设备在线监测系统、水机自动装置及自动化元件",
            "起重设备控制系统、辅助设备自动控制系统",
            "调速器及油压装置（含圆筒阀油压装置）、励磁系统",
        ],
    },
    {
        "major": "坝工",
        "groups": [
            "水工建筑物、库区设施、水情测报系统",
        ],
    },
]


def init_data():
    for l in Labels:
        major = l['major']
        groups = l['groups']
        r1 = SysDict.query.filter(SysDict.item_text == major).first()
        r1_id = r1.item_value 
        for g in groups:
            mst = MstTag()
            mst.name = g
            mst.type = int(r1_id)
            db.session.add(mst)
    db.session.commit()

# init_data()