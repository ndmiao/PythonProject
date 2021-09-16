# -*- coding: utf-8 -*-
"""
@Time ： 2021/9/15 14:30
@Auth ： ndmiao
@Blog ：www.ndmiao.cn
"""

import json
import requests
from GetSecret import GetConnect

class SendMessage:
    def __init__(self):
        self.url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.filename = 'message.json'

    # 读取消息结构配置
    def get_message_structure(self):
        with open(self.filename, "r") as f:
            structure = json.load(f)
        return structure

    # 根据不同的type选择不同的消息
    def deal_message(self, msgtype, content):
        structure = self.get_message_structure()
        messageConfig = GetConnect().get_local_config()
        # 发送文本格式的消息
        if msgtype == 'text':
            message = structure['text']
            message['text']['content'] = content
        # 发送markdown格式的消息
        elif msgtype == 'markdown':
            message = structure['markdown']
            message['markdown']['content'] = content
        message['touser'] = messageConfig['touser']
        message['agentid'] = messageConfig['agentid']
        return message

    # 发送消息
    def send_message(self, msgtype, content):
        access_token = GetConnect().get_result()
        url = self.url + access_token
        message = self.deal_message(msgtype, content)
        raw_data = json.dumps(message)
        res = requests.post(url=url, data=raw_data)
        return res

if __name__ == "__main__":
    SendMessage().send_message('markdown','>**事项详情**')