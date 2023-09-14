import requests
from urllib.parse import urlencode
import json
from datetime import datetime
import os
import ast
import urllib.parse
import urllib.request

def sc_send(title, content, key):
  postdata = urllib.parse.urlencode({'text': title, 'desp': content}).encode('utf-8')
  url = f'https://sctapi.ftqq.com/{key}.send'
  req = urllib.request.Request(url, data=postdata, method='POST')
  with urllib.request.urlopen(req) as response:
    result = response.read().decode('utf-8')
  return result

def main_handler(event, context):
  url = 'https://nodeoj.com/qiandao/ouhuang'

  # cookies = {'ssid': '你的nodeoj的cookies'}
  cookies = { 'ssid': os.environ.get('COOKIES') }

  headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://nodeoj.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
  }

  params = {'foo': 'bar'}

  response = requests.get(url, cookies=cookies, headers=headers, params=params)

  response_text = response.text
  data = json.loads(response_text)

  status = data['status']
  text = status.replace('<br/>','\n\n')

  # 获取的时间戳并非签到时间
  # if 'time' in data:
  #   dt = datetime.fromisoformat(data['time'][:-1])
  #   text += '签到时间:' + dt.strftime('%Y-%m-%d %H:%M:%S')

  key = os.environ.get('KEY')
  # key = '你的server酱sendkey'

  ret = sc_send('签到结果', text, key)
  print(ret)

if __name__ == '__main__':
  main_handler(None, None)
