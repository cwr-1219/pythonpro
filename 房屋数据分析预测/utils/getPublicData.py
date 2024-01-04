from model.Hourse_info import Hourse_info
import json
from datetime import datetime
from db import db
from model.History import History
from model.Usser import User
from utils.query import querys
cityList = [
    {'province': '北京', 'city':['北京市']},
    {'province': '天津', 'city': ['天津市']},
    {'province': '河北', 'city': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市']},
    {'province': '山西', 'city': ['太原市','大同市','朔州市','忻州市','阳泉市','晋中市','吕梁市','长治市','临汾市','晋城市','运城市']},
    {'province': '内蒙古', 'city': ['呼和浩特市','呼伦贝尔市','通辽市','赤峰市','巴彦淖尔市','乌兰察布市','包头市','鄂尔多斯市','乌海市',  '兴安盟', '锡林郭勒盟', '阿拉善盟']},
    {'province': '辽宁', 'city': ['沈阳市','铁岭市','阜新市','抚顺市','朝阳市','本溪市','辽阳市','鞍山市','盘锦市','锦州市','葫芦岛市','营口市','丹东市','大连市']},
    {'province': '吉林', 'city': ['长春市','白城市','松原市','吉林市','四平市','辽源市','白山市','通化市','延边']},
    {'province': '黑龙江', 'city': ['哈尔滨市','黑河市','伊春市','齐齐哈尔市','鹤岗市','佳木斯市','双鸭山市','绥化市','大庆市','七台河市','鸡西市','牡丹江市', '大兴安岭地区']},
    {'province': '上海', 'city': ['上海市']},
    {'province': '江苏', 'city': ['南京市','连云港市','徐州市','宿迁市','淮安市','盐城市','泰州市','扬州市','镇江市','南通市','常州市','无锡市','苏州市']},
    {'province': '浙江', 'city': ['杭州市','湖州市','嘉兴市','绍兴市','舟山市','宁波市','金华市','衢州市','台州市','丽水市','温州市']},
    {'province': '安徽', 'city': ['合肥市','淮北市','亳州市','宿州市','蚌埠市','阜阳市','淮南市','滁州市','六安市','马鞍山市','芜湖市','宣城市','铜陵市','池州市','安庆市','黄山市']},
    {'province': '福建', 'city': ['福州市','宁德市','南平市','三明市','莆田市','龙岩市','泉州市','漳州市','厦门市']},
    {'province': '江西', 'city': ['南昌市','九江市','景德镇市','上饶市','鹰潭市','抚州市','新余市','宜春市','萍乡市','吉安市','赣州市']},
    {'province': '山东',
     'city': ['济南市','德州市','滨州市','东营市','烟台市','威海市','淄博市','潍坊市','聊城市','泰安市','莱芜市','青岛市','日照市','济宁市','菏泽市','临沂市','枣庄市']},
    {'province': '河南',
     'city': ['郑州市','安阳市','鹤壁市','濮阳市','新乡市','焦作市','三门峡市','开封市','洛阳市','商丘市','许昌市','平顶山市','周口市','漯河市','南阳市','驻马店市','信阳市']},
    {'province': ' 湖北',
     'city': ['武汉市','十堰市','襄樊市','随州市','荆门市','孝感市','宜昌市','黄冈市','鄂州市','荆州市','黄石市','咸宁市']},
    {'province': '湖南',
     'city': ['长沙市','岳阳市','张家界市','常德市','益阳市','湘潭市','株洲市','娄底市','怀化市','邵阳市','衡阳市','永州市','郴州市']},
    {'province': '广东',
     'city': ['广州市','韶关市','梅州市','河源市','清远市','潮州市','揭阳市','汕头市','肇庆市','惠州市','佛山市','东莞市','云浮市','汕尾市','江门市','中山市','深圳市','珠海市','阳江市','茂名市','湛江市']},
    {'province': '广西',
     'city': ['南宁市','桂林市','河池市','贺州市','柳州市','百色市','来宾市','梧州市','贵港市','玉林市','崇左市','钦州市','防城港市','北海市']},
    {'province': '海南', 'city': ['海口市','三亚市','三沙市','儋州市','五指山市','文昌市','琼海市','万宁市','东方市']},
    {'province': '重庆', 'city': ['重庆市']},
    {'province': '四川',
     'city': ['成都市','广元市','巴中市','绵阳市','德阳市','达州市','南充市','遂宁市','广安市','资阳市','眉山市','雅安市','内江市','乐山市','自贡市','泸州市','宜宾市','攀枝花市']},
    {'province': '贵州', 'city': ['贵阳市','遵义市','六盘水市','安顺市','铜仁市','毕节市']},
    {'province': '云南', 'city': ['昆明市','昭通市','丽江市','曲靖市','保山市','玉溪市','临沧市','普洱市']},
    {'province': '西藏自治区', 'city': ['拉萨市','日喀则市','昌都市','林芝市','山南市','那曲市']},
    {'province': '陕西', 'city': ['西安市','榆林市','延安市','铜川市','渭南市','宝鸡市','咸阳市','商洛市','汉中市','安康市']},
    {'province': '甘肃', 'city': ['兰州市','嘉峪关市','酒泉市','张掖市','金昌市','武威市','白银市','庆阳市','平凉市','定西市','天水市','陇南市']},
    {'province': '青海', 'city': ['西宁市','海东市','海北','黄南', '海南', '果洛', '玉树', '海西']},
    {'province': '宁夏回族自治区', 'city': ['银川市','石嘴山市','吴忠市','中卫市','固原市']},
    {'province': '新疆维吾尔自治区',
     'city': ['乌鲁木齐市','库尔勒市','吐鲁番市','克拉玛依市','阿勒泰市','五家渠市','阿拉尔市','图木舒克市','北屯市','铁门关市','喀什市','阿克苏市','和田市','阿图什市','博乐市','阿拉山口市','昌吉市','阜康市','伊宁市','米泉市','奎屯市','塔城市','乌苏市','石河子市','哈密市']},
    {'province': '台湾',
     'city': ['台北市', '高雄市' , '台南市' ,'台中市','金门县', '南投县','基隆市','新竹市','嘉义市','新北市','宜兰县','新竹县','桃园县','黄栗县','彰化县','嘉义县','云林县','屏东县','台东县','花莲县','壹湖县','连江县']},
    {'province': '香港特别行政区', 'city': ['香港岛','香港岛','新界']},
    {'province': '澳门特别行政区', 'city': ['澳门','离岛']},

]

def getUserHistoryData(username):
    user = querys('select * from user  where user_name = %s', [username],'select')[0]
    hisotryList = querys('select * from history where user_id = %s', [int(user[0])], 'select')
    maxPrice = 0
    lastcity = None
    cityLenDic = {}
    for h in hisotryList:
        if maxPrice < float(h[2]):maxPrice = float(h[2])
        if cityLenDic.get(h[1],-1) == -1:
            cityLenDic[h[1]] = 1
        else:
            cityLenDic[h[1]] += 1
        lastcity = h[1]
        lastPrice = float(h[2])
    sortCityLen = list(sorted(cityLenDic.items(), key=lambda x:x[1], reverse=True))
    return hisotryList, len(hisotryList),maxPrice,sortCityLen[0][0], lastcity,lastPrice

def getAllHourse_infoMap(city=''):
    if city:
        hourseList = Hourse_info.query.filter_by(city=city).all()
    else:
        hourseList = Hourse_info.query.all()

    def map_fn(item):
        item.rooms_desc = json.loads(item.rooms_desc)
        item.area_range = json.loads(item.area_range)
        item.tags = json.loads(item.tags)
        item.totalPrice_range = json.loads(item.totalPrice_range)
        return item
    hourseListMap = list(map(map_fn,hourseList))
    return hourseListMap

def getHourseInfoById(id):
    hourseInfo = Hourse_info.query.filter_by(id=id).first()
    hourseInfo.rooms_desc = json.loads(hourseInfo.rooms_desc)
    hourseInfo.tags = json.loads(hourseInfo.tags)
    hourseInfo.area_range = json.loads(hourseInfo.area_range)
    hourseInfo.totalPrice_range = json.loads(hourseInfo.totalPrice_range)
    return hourseInfo
def addHisotry(city,price,username):
    user = Usser.query.filter_by(username = username).first()
    newHistory = History(city=city, price=price, user=user)
    db.session.add(newHistory)
    db.session.commit()

def addHourseInfo(hourseInfo):
    hourseInfo['rooms_desc'] = json.dumps(hourseInfo['rooms_desc'].split('，'))
    hourseInfo['area_range'] = json.dumps(hourseInfo['area_range'].split('-'))
    hourseInfo['tags'] = json.dumps(hourseInfo['tags'].split('，'))
    hourseInfo['all_ready'] = '1'
    hourseInfo['on_time'] = '0000-00-00 00:00:00'
    hourseInfo['totalPrice_range'] = json.dumps([0])
    hourseInfo['sale_status'] = '1'
    hourseInfo['detail_url'] = '0'
    now = datetime.now()
    hourseInfo['open_date'] = f"{now.year}-{now.month:02d}-{now.day:02d}"
    hourse = Hourse_info(
        title=hourseInfo['title'],city=hourseInfo['city'],region=hourseInfo['region'],
        address=hourseInfo['address'],rooms_desc=hourseInfo['rooms_desc'],area_range=hourseInfo['area_range'],
        price=hourseInfo['price'],hourseDecoration=hourseInfo['hourseDecoration'],
        company=hourseInfo['company'],hourseType=hourseInfo['hourseType'],
        all_ready=hourseInfo['all_ready'],
        on_time=hourseInfo['on_time'],
        open_date=hourseInfo['open_date'],tags=hourseInfo['tags'],cover=hourseInfo['cover'],
        totalPrice_range=hourseInfo['totalPrice_range'],
        sale_status=hourseInfo['sale_status'],detail_url=hourseInfo['detail_url'],
    )
    db.session.add(hourse)
    db.session.commit()

def editHourseInfo(hourseInfo, id):
    hourseInfo['rooms_desc'] = json.dumps(hourseInfo['rooms_desc'].split('，'))
    hourseInfo['area_range'] = json.dumps(hourseInfo['area_range'].split('-'))
    hourseInfo['tags'] = json.dumps(hourseInfo['tags'].split('，'))
    hourse = getHourseInfoById(id)
    hourse.title = hourseInfo['title']
    hourse.city = hourseInfo['city']
    hourse.region = hourseInfo['region']
    hourse.address = hourseInfo['address']
    hourse.rooms_desc = hourseInfo['rooms_desc']
    hourse.area_range = hourseInfo['area_range']
    hourse.price = hourseInfo['price']
    hourse.hourseDecoration = hourseInfo['hourseDecoration']
    hourse.company = hourseInfo['company']
    hourse.hourseType = hourseInfo['hourseType']
    hourse.tags = hourseInfo['tags']
    if hourseInfo['cover'] != '0':
        hourse.cover = hourseInfo['cover']
    db.session.commit()

def deleteHourseInfo(id):
    hourseInfo = getHourseInfoById(id)
    db.session.delete(hourseInfo)
    db.session.commit()

def getCitiesList():
    hourseList = list(set([x.city for x in Hourse_info.query.all() if x.city]))
    return hourseList
