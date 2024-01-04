import  requests
from lxml import etree
import csv
import os


def writerRow(row):
    with open('./cityData.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def init():
    if not os.path.exists('./cityData.csv'):
        with open('./cityData.csv','w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'city',
                'cityLink'
            ])

def get_html(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_html(html):
    root = etree.HTML(html)
    cityList = root.xpath('//div[@class="fc-main clear"]//li[@class="clear"]//a')
    for city in cityList:
        cityName = city.text
        cityLink = city.get('href') + '/loupan/pg1/?_t=1'
        writerRow([
            cityName,
            cityLink
        ])


def main():
    init()
    url = 'https://bh.fang.lianjia.com/loupan/pg2/'
    html = get_html(url)
    parse_html(html)

if __name__ == '__main__':
    main()