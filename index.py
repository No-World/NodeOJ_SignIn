import requests
from urllib.parse import urlencode
import json
from datetime import datetime
import os
import ast
import urllib.parse
import urllib.request


def main_handler(event, context):
    key = os.environ.get('KEY')
    # key = '你的server酱sendkey'
    cookies = {'ssid': os.environ.get('COOKIES')}
    # cookies = {'ssid': '你的nodeoj的cookies'}

    ret = sc_send('签到结果', signin(cookies), key)
    print(ret)


def signin(cookies):
    url = 'https://nodeoj.com/qiandao/ouhuang'

    headers = {'User-Agent': 'No_World签到姬'.encode('utf-8')}
    response = requests.get(url, cookies=cookies, headers=headers)
    response_text = response.text
    data = json.loads(response_text)
    status = data['status']
    text = status.replace('<br/>', '\n\n')

    # 获取的时间戳并非签到时间
    # if 'time' in data:
    #   dt = datetime.fromisoformat(data['time'][:-1])
    #   text += '签到时间:' + dt.strftime('%Y-%m-

    return text


def sc_send(title, content, key):
    postdata = urllib.parse.urlencode({'text': title, 'desp': content}).encode('utf-8')
    url = f'https://sctapi.ftqq.com/{key}.send'
    req = urllib.request.Request(url, data=postdata, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
    return result


if __name__ == '__main__':
    main_handler(None, None)
