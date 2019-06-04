import requests
import re
import json
from requests.exceptions import RequestException
from multiprocessing import Pool
def get_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None
def parse_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name"><a.*?">(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'name':item[1],
            'actor':item[2].strip()[3:],
            'time':item[3][5:],
            '评分':item[4]+item[5]
        }
def write_into_file(content):
    with open('read5.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
def main(os):
    url='https://maoyan.com/board/4?os='+str(os)
    html=get_page(url)
    for item in parse_page(html):
        print(item)
        write_into_file(item)
if __name__ == '__main__':
    pool=Pool()
    pool.map(main,[x*10 for x in range(10)])

