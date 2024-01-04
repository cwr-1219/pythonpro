from utils.getPublicData import cityList
from model.Hourse_info import Hourse_info

def getHomeGeoCharData(hourse_data):
    average_price_dic = average_price(hourse_data)
    cityDic = {}
    for key ,value in average_price_dic.items():
        for j in cityList:
            for k in j['city']:
                if k.find(key) != -1:
                    cityDic[j['province']] = value
    cityDicList = []
    for key, value in cityDic.items():
        cityDicList.append({
            'name':key,
            'value':value
        })
    return cityDicList

def getHomeRadarData(hourse_data):
    cityDic = {}
    for i in hourse_data:
        if cityDic.get(i.city, -1) == -1:
            cityDic[i.city] = 1
        else:
            cityDic[i.city] += 1
    # print(cityDic)
    radarOne = []
    radarTwo = list(cityDic.values())
    for key, value in cityDic.items():
        radarOne.append({
            'name': key,
            'max': 100
        })
    return radarOne, radarTwo

def getHomeTagsData(hourse_data):
    maxPrice = 0
    maxHourseType = {}
    maxHourseSale_status = {}
    for i in hourse_data:
        if i.price and maxPrice < int(i.price):
            maxPrice = int(i.price)
        if maxHourseType.get(i.hourseType, -1) == -1:
            maxHourseType[i.hourseType] = 1
        else:
            maxHourseType[i.hourseType] += 1

        if maxHourseSale_status.get(i.sale_status, -1) == -1:
            maxHourseSale_status[i.sale_status] = 1
        else:
            maxHourseSale_status[i.sale_status] += 1
    maxHourseTypeSort = list(sorted(maxHourseType.items(), key=lambda x:x[1], reverse=True))
    maxHourseSale_statusSort = list(sorted(maxHourseSale_status.items(), key=lambda x:x[1], reverse=True))
    maxHourseSale = ''
    if maxHourseSale_statusSort[0][0] == '1':
        maxHourseSale = '在售'
    elif maxHourseSale_statusSort[0][0] == '2':
        maxHourseSale = '已售'
    elif maxHourseSale_statusSort[0][0] == '3':
        maxHourseSale = '出租中'
    elif maxHourseSale_statusSort[0][0] == '4':
        maxHourseSale = '已出租'
    elif maxHourseSale_statusSort[0][0] == '5':
        maxHourseSale = '预售'
    elif maxHourseSale_statusSort[0][0] == '6':
        maxHourseSale = '其他'


    return  len(hourse_data), maxPrice, maxHourseTypeSort[0][0], maxHourseSale

def getHourseByHourseName(searchWord, hourse_data):
   searchList = []
   for hourse in hourse_data:
       if hourse.title.find(searchWord) != -1:
        searchList.append(hourse)
   return searchList



def average_price(hourse_data):
    city_prices = {}
    city_counts = {}
    for house in hourse_data:
        city = house.city
        price = house.price
        if price:
            try:
                prices = int(house.price)
            except ValueError:
                pass
        else:
            pass
        if city in city_prices:
            city_prices[city] += prices
            city_counts[city] += 1
        else:
            city_prices[city] = prices
            city_counts[city] = 1

    average_prices = {}
    for city in city_prices:
        average_prices[city] = round(city_prices[city] / city_counts[city], 1 )

    return  average_prices

def getPriceCharDataOne(hourseList):
    X = ['<=4000', '4000-6000','6000-8000','8000-10000','10000-12000','12000-15000','15000-18000','>18000',]
    Y = [0 for x in range(len(X))]
    for h in hourseList:
        if int(h.price) <=4000:
            Y[0] += 1
        elif int(h.price) <=6000:
            Y[1] += 1
        elif int(h.price) <=8000:
            Y[2] += 1
        elif int(h.price) <=10000:
            Y[3] += 1
        elif int(h.price) <=12000:
            Y[4] += 1
        elif int(h.price) <=15000:
            Y[5] += 1
        elif int(h.price) <=18000:
            Y[6] += 1
        elif int(h.price) >18000:
            Y[7] += 1
    return X,Y

def getPriceCharDataTWo(houreList):
    open_dataDic={}
    for h in houreList:
        if open_dataDic.get(h.open_date, -1) == -1:
            open_dataDic[h.open_date] = int(h.price)
        else:
            open_dataDic[h.open_date] += int(h.price)

    return list(open_dataDic.keys()),list(open_dataDic.values())


def getPriceCharDataThree(houreList):
    data = []
    for h in houreList:
        data.append(
            h.totalPrice_range
        )
    return data

def getDetailCharone(hourseList):
    roomsDic = {}
    for i in hourseList:
        for room in i.rooms_desc:
            if roomsDic.get(room, -1) == -1:
                roomsDic[room] = 1
            else:
                roomsDic[room] += 1
    result = []
    for key, value in roomsDic.items():
        result.append({
            'name': key,
            'value': value
        })
        return result

def getDetailCharTwo(hourseList, defaultType):
    if defaultType == 'big':
        X = [
            '80-100',
            '100-110',
            '110-120',
            '120-130',
            '130-140',
            '140-150',
            '150-160',
            '160-n'
        ]
        Y = [0 for x in range(len(X))]
        for i in hourseList:
            try:
                if int(i.area_range[1]) < 100:
                    Y[0] += 1
                elif int(i.area_range[1]) < 110:
                    Y[1] += 1
                elif int(i.area_range[1]) < 120:
                    Y[2] += 1
                elif int(i.area_range[1]) < 130:
                    Y[3] += 1
                elif int(i.area_range[1]) < 140:
                    Y[4] += 1
                elif int(i.area_range[1]) < 150:
                    Y[5] += 1
                elif int(i.area_range[1]) > 160:
                    Y[6] += 1
            except:
                continue
    elif defaultType == 'small':
        X = [
            '0-40',
            '40-60',
            '60-80',
            '80-100',
            '100-120',
            '120-150',
            '150-n' ]
        Y = [0 for x in range(len(X))]
        for i in hourseList:
            try:
                if int(i.area_range[0]) < 40:
                    Y[0] += 1
                elif int(i.area_range[0]) < 60:
                    Y[1] += 1
                elif int(i.area_range[0]) < 80:
                    Y[2] += 1
                elif int(i.area_range[0]) < 100:
                    Y[3] += 1
                elif int(i.area_range[0]) < 120:
                    Y[4] += 1
                elif int(i.area_range[0]) < 150:
                    Y[5] += 1
                elif int(i.area_range[0]) >= 150:
                    Y[6] += 1
            except:
                continue


    return X,Y
def getDicData(hourseList,fild):
    hourseDecorationDic = {}
    for h in hourseList:
        if fild =='hourseDecoration' and h.hourseDecoration !='':
            if hourseDecorationDic.get(h.hourseDecoration,-1) == -1:
                hourseDecorationDic[h.hourseDecoration] = 1
            else:
                hourseDecorationDic[h.hourseDecoration] += 1
        elif fild == 'hourseType':
            if hourseDecorationDic.get(h.hourseType,-1) == -1:
                hourseDecorationDic[h.hourseType] = 1
            else:
                hourseDecorationDic[h.hourseType] += 1
        elif fild == 'tags':
            for tag in h.tags:
                if hourseDecorationDic.get(tag, -1) == -1:
                    hourseDecorationDic[tag] = 1
                else:
                    hourseDecorationDic[tag] += 1


    resData = []
    for key, value in hourseDecorationDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getTypeCharDataOne(hourseList):
      return getDicData(hourseList,'hourseDecoration')

def getTypeCharDataTwo(hourseList):
    return getDicData(hourseList, 'hourseType')
def grtAnotherCharOne(hourseList):
    cityDic = {}
    for i in hourseList:
        if i.on_time == '0000-00-00 00:00:00':
            if cityDic.get(i.city, -1) == -1:
                cityDic[i.city] = 1
            else:
                cityDic[i.city] += 1
    return list(cityDic.keys()), list(cityDic.values())

def getAnotherCharTwo(hourseList):
    sale_satusDic = {}
    for h in hourseList:
            if h.sale_status == '1':
                if sale_satusDic.get('在售', -1) == -1:
                    sale_satusDic['在售'] = 1
                else:
                    sale_satusDic['在售'] += 1
            elif h.sale_status == '2':
                if sale_satusDic.get('已售', -1) == -1:
                    sale_satusDic['已售'] = 1
                else:
                    sale_satusDic['已售'] += 1
            elif h.sale_status == '3':
                if sale_satusDic.get('出租中', -1) == -1:
                    sale_satusDic['出租中'] = 1
                else:
                    sale_satusDic['出租中'] += 1

            elif h.sale_status == '4':
                if sale_satusDic.get('已出租', -1) == -1:
                    sale_satusDic['已出租'] = 1
                else:
                    sale_satusDic['已出租'] += 1
            elif h.sale_status == '5':
                if sale_satusDic.get('预售', -1) == -1:
                    sale_satusDic['预售'] = 1
                else:
                    sale_satusDic['预售'] += 1
            elif h.sale_status == '6':
                if sale_satusDic.get('其他', -1) == -1:
                    sale_satusDic['其他'] = 1
                else:
                    sale_satusDic['其他'] += 1
    resData = []
    for key, value in sale_satusDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getAnotherCharThree(hourseList):
    return [x['name'] for x in getDicData(hourseList, 'tags')],[x['value'] for x in getDicData(hourseList, 'tags')]




