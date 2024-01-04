import csv
import re
import os
import sys
import requests
import json
from pymysql import *
from utils.query import querys



# 房名 封面 市区 地区 详情地址 房型详情 建面 是否具有预售证 每平价格 房屋的装修情况（毛胚，简装修） 公司 房屋类型（别墅） 交房时间 开盘时间 标签 总价区间（在售） 详情链接

def init():
    if not os.path.exists('./hourseInfoData.csv'):
        with open('./hourseInfoData.csv','w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'title',
                'cover',
                'city',
                'region',
                'address',
                'room_desc',
                'area_range',
                'all_ready',
                'price',
                'houseDecoration',
                'company',
                'hourseType',
                'on_time',
                'open_date',
                'tags',
                'totalPrice_range',
                'sale_status',
                'detail_url'

            ])

def writerRow(row):
    with open('./hourseInfoData.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def get_data(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'cookie':'lianjia_uuid=303a5f2a-86c4-45fe-9f71-c9df99838827; _ga=GA1.2.933300983.1700384112; _gid=GA1.2.1541903017.1700384112; _jzqc=1; _jzqckmp=1; lianjia_ssid=d4b88ec7-ff94-a37d-8e87-f61131b8c72f; select_city=340100; b-user-id=903b32ee-4bf7-a1cd-de91-bfb4dc123810; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _jzqa=1.1323699580604419000.1700384112.1700384112.1700388741.2; _jzqx=1.1700388741.1700388741.1.jzqsr=bh%2Efang%2Elianjia%2Ecom|jzqct=/.-; _qzjc=1; digData=%7B%22key%22%3A%22loupan_index%22%7D; _qzja=1.1375958557.1700388741524.1700388741524.1700388741525.1700388741525.1700388743485.0.0.0.2.1; _qzjb=1.1700388741524.2.0.0.0; _qzjto=2.1.0; _jzqb=1.2.10.1700388741.1; srcid=eyJ0IjoiXCJ7XFxcImRhdGFcXFwiOlxcXCJhODM2MWVhNGYyYzllY2E3OWNmYmQ3OWQ3MzdlMTNiOWZhYjllZTY1MzU3MWUzMmZmMzA5YTFhNjU3MjIwZTA0ZTIwODZjNGVlMWUyZjY4ZDU5NmY1YWRmMmMzNmQyZDUyNjVmMjNjMjkxMmJmZDk4MWUxZTJhZTgwYmVlN2QyMTgyOGJmNTE3MjVkODNlYTA1MDA4ZDhjYzAyYzQ5NDI5MTg1N2RhMTlkNGY3NmY3YTAzZjMwYjE4YzAzZTZmZDEzNWFjNmE1MGMyMzc2Yjc2YzI5N2FhMjg0OTVlZTdkMzM5NGUwZDYyYTY1ZDRkMmIyMGNiYWZhMzA3OWNiNzljXFxcIixcXFwia2V5X2lkXFxcIjpcXFwiMVxcXCIsXFxcInNpZ25cXFwiOlxcXCJhY2I1YzBlYlxcXCJ9XCIiLCJyIjoiaHR0cHM6Ly9oZi5mYW5nLmxpYW5qaWEuY29tL2xvdXBhbi8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; lj_newh_session=eyJpdiI6IkNPZWxwRk12c29FMUtkRUlIRStyT1E9PSIsInZhbHVlIjoiNHR2a0NCNlViNGluWFJDb2lBekhmR2NxK3FSeGJrZWVKbm9kemhnVzV1TktYcTFCM2doNTlcL1MxeXZcL21sYVwvVW5iZVFJR2p0UGlQM2tuZ3J5ZEVVbkE9PSIsIm1hYyI6ImQ5NTliZDU5NzExNjI1MjJhMzRlMGQ5MDMxNmExYzJhM2Q1MzM3MGMxMjU2ZmQxNjVlMTNjNTMxN2VmMDY2YjYifQ%3D%3D',
        'Referer': 'https://hf.fang.lianjia.com/loupan/pg1/'
    }
    response = requests.get(url, headers)
    if response.status_code == 200:
        # print(response.json())
        return response.json()['data']['list']
    else:
        return None

#     解析
# 房名 封面 市区 地区 详情地址 房型详情 建面 是否具有预售证 每平价格 房屋的装修情况（毛胚，简装修） 公司 房屋类型（别墅） 交房时间 开盘时间 标签 总价区间（在售） 详情链接

def parse_data(hourseDetailList , city, url):
    for hourseInfo in hourseDetailList:
        try:
            title = hourseInfo['title']
            cover = hourseInfo['cover_pic']
            region = hourseInfo['district']
            address = hourseInfo['address']
            room_desc = json.dumps(hourseInfo['frame_rooms_desc'].replace('居', '').split('/'))
            area_range = json.dumps(hourseInfo['resblock_frame_area_range'].replace('㎡', '').split('-'))
            all_ready = hourseInfo['permit_all_ready']
            price = hourseInfo['average_price']
            houseDecoration = hourseInfo['decoration']
            company = hourseInfo['developer_company'][0]
            hourseType = hourseInfo['house_type']
            on_time = hourseInfo['on_time']
            open_date = hourseInfo['open_date']
            tags = json.dumps(hourseInfo['tags'])
            totalPrice_range = json.dumps(hourseInfo['reference_total_price'].split('-'))
            sale_status = hourseInfo['process_status']
            detail_url = 'https://' + re.search('//(.*)/loupan/pg\d/\?_t=1', url).group(1) + hourseInfo['url']
            writerRow([
                title,
                cover,
                city,
                region,
                address,
                room_desc,
                area_range,
                all_ready,
                price,
                houseDecoration,
                company,
                hourseType,
                on_time,
                open_date,
                tags,
                totalPrice_range,
                sale_status,
                detail_url

            ])
        except:
            continue

def save_to_sql():
    with open('./hourseInfoData.csv', 'r', encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(readerCsv)
        for h in readerCsv:
            querys('''
                    insert into hourse_info(title,cover,city,region,address,rooms_desc,area_range,all_ready,price,hourseDecoration,company,hourseType,on_time,open_date,tags,totalPrice_range,sale_status,detail_url)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',[
                h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15], h[16], h[17]
            ])



def main():
    init()
    with open('./cityData.csv', 'r', encoding='utf-8')as  readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for city in reader:
            for page in range(1, 10):
                try:
                  url = 'https:' + re.sub('pg1', 'pg' + str(page), city[1])
                  print('正在爬取 %s 城市的房屋数据正在第 %s 页 路径为：%s' % (
                      city[0],
                      page,
                      url
                  ))
                  hourseDetailList = get_data(url)
                  parse_data(hourseDetailList, city[0], url)
                except:
                    pass
#                 换成continue可以在官方又有些链接打不开的到时候用 会跳过




if __name__ == '__main__':
    # main()
    save_to_sql()