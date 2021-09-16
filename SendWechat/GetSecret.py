# -*- coding: utf-8 -*-
"""
@Time ： 2021/9/7 14:15
@Auth ： ndmiao
@Blog ：www.ndmiao.cn
"""

import json
import requests
from datetime import datetime

class GetConnect:
    def __init__(self):
        self.url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.filename = 'config.json'

    # 读取本地的json文件的配置
    def get_local_config(self):
        with open(self.filename, "r") as f:
            myConfig = json.load(f)
        return myConfig

    # 存储json配置
    def save_local_config(self, myConfig):
        with open(self.filename, "w") as f:
            json.dump(myConfig, f)

    # 测试时间差
    def get_time_differ(self):
        myConfig = self.get_local_config()
        timeNow = datetime.now()  # 获取现在的时间
        timeNow = timeNow.strftime("%Y-%m-%d %H:%M:%S") # 转换成相应格式的字符串
        timeLast = myConfig['refresh_time']
        timeNow = datetime.strptime(timeNow, "%Y-%m-%d %H:%M:%S")
        timeLast = datetime.strptime(timeLast,"%Y-%m-%d %H:%M:%S")
        timeDiffer = timeNow - timeLast
        return timeDiffer.total_seconds()


    # 获取企业微信程序的access_token
    def get_access_token(self):
        myConfig = self.get_local_config()
        # 拼接得到url
        urls = self.url + 'corpid=' + myConfig['corpid'] + '&corpsecret=' + myConfig['corpsecret']
        res = requests.get(urls).json()
        access_token = res['access_token']
        return access_token

    # 7200S即两小时更新一次access_token
    def get_result(self):
        myConfig = self.get_local_config()
        timeDiffer = self.get_time_differ()
        if timeDiffer > 7200:
            access_token = self.get_access_token()
            myConfig['access_token'] = access_token
            myConfig['refresh_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_local_config(myConfig)
        else:
            access_token = myConfig['access_token']
        return access_token

if __name__ == "__main__":
    print(GetConnect().get_result())
