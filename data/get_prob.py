import requests
from lxml import etree

url = 'https://www.luogu.com.cn/problem/list?difficulty=6&type=AT&page='
n = 11

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

for i in range(1, n + 1):
    res = requests.get(url + str(i), headers=headers)
    res.encoding = 'utf-8'
    ele = etree.HTML(res.text)
    lst = ele.xpath('//li/text()')

    with open(f"at.txt", "a", encoding='utf-8') as f:
        for name in lst:
            f.write(name[:-1] + ',')

    print(f"page {i} done.")
