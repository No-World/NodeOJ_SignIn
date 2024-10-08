import requests
from urllib.parse import urlencode
import json
from datetime import datetime
import os
import ast
import urllib.parse
import urllib.request


def handler(event, context):
    key = os.environ.get('KEY')
    # key = '你的server酱SendKey'
    cookies = {'ssid': os.environ.get('COOKIES')}
    # cookies = {'ssid': '你的NodeOJ的cookies'}

    if cookies['ssid'] is None:
        print('未配置NodeOJ的cookies, 签到失败, 请查看README文档配置后重试')
        return

    else:
        info = signin(cookies)
        print('签到结果:\n' + info)

        if key is None:
            print('未配置server酱的SendKey, 如有需要请查看README文档配置后重试')
        else:
            # 将结果推送到server酱
            ret = sc_send('签到结果', info, key)
            print(ret)


def signin(cookies):
    url = 'https://nodeoj.com/qiandao/ouhuang'
    headers = {'User-Agent': 'No_World签到姬'.encode('utf-8')}
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()
        if response.headers['Content-Type'].startswith('text/html'):
            return 'NodeOJ：登陆失败，请检查cookies'
        response_text = response.text
        data = json.loads(response_text)
        status = data['status']
        text = status.replace('<br/>', '\n\n')

        # 获取的时间戳并非签到时间
        # if 'time' in data:
        #   dt = datetime.fromisoformat(data['time'][:-1])
        #   text += '签到时间:' + dt.strftime('%Y-%m-%d %H:%M:%S')

    except:
        return 'NodeOJ请求失败！'

    return text


def sc_send(title, content, key):
    postdata = urllib.parse.urlencode({'text': title, 'desp': content}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result


# 调试用程序入口
if __name__ == '__main__':
    handler(None, None)
