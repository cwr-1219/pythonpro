from flask import Flask,session,render_template,redirect,Blueprint,request
from utils.getPageData import *
from utils.getPublicData import getAllHourse_infoMap, getHourseInfoById,addHourseInfo,editHourseInfo,deleteHourseInfo,getCitiesList,getUserHistoryData
import random
import uuid
import os
from pred.index import create_engine,train_test_split
from app import app
pb = Blueprint('page', __name__, url_prefix='/page' , template_folder='templates' )

@pb.route('/home')
def home():
    username = session.get('username')
    hourse_data =  getAllHourse_infoMap()
    getCharData = getHomeGeoCharData(hourse_data)
    result = getDetailCharone(hourse_data)
    defaultType = request.args.get('type') if request.args.get('type') else 'small'
    X,Y = getDetailCharTwo(hourse_data,defaultType)
    hourse_dataLen, maxPrice, maxHourseType, maxHourseSale = getHomeTagsData(hourse_data)
    radarOne, radarTwo =  getHomeRadarData(hourse_data)
    historyList,predMax,maxPricePre,maxCity, lastcity, lastPrice = getUserHistoryData(username)


    return render_template('index.html',
                           username=username,
                           getCharData=getCharData,
                           hourse_dataLen = hourse_dataLen,
                           maxPrice = maxPrice,
                           maxHourseType = maxHourseType,
                           maxHourseSale =maxHourseSale,
                           radarOne = radarOne,
                           radarTwo = radarTwo,
                           historyList = historyList,
                           predMax=predMax,
                           maxPricePre=maxPricePre,
                           maxCity=maxCity,
                           lastcity=lastcity,
                           lastPrice=lastPrice,
                           result=result,
                           X=X,
                           Y=Y)

@pb.route('/search', methods=['GET', 'POST'] )
def search():
    username = session.get('username')
    hourse_data =  getAllHourse_infoMap()
    maxLen = len(hourse_data)
    if request.method == 'GET':
        # 或者直接放hourse_data
        hourseListRandom = [hourse_data[random.randint(0,maxLen)] for x in range(8)]
        cities = [x.city for x in hourseListRandom]
    else:
        hourseListRandom = getHourseByHourseName(request.form['searchWord'], hourse_data)
        cities = [x.city for x in hourseListRandom]

    return render_template('search.html',
                           username=username,
                           cities = cities,
                           hourseListRandom = hourseListRandom
                           )

@pb.route('/tableData', methods=['GET', 'POST'] )
def tableData():
    username = session.get('username')
    hourse_data =  getAllHourse_infoMap()[:50]
    return render_template('tableData.html',
                           username=username,
                           hourse_data = hourse_data
                           )
@pb.route('/detail', methods=['GET', 'POST'] )
def detail():
    username = session.get('username')
    id = request.args.get('id')
    hourseInfo = getHourseInfoById(id)
    # hourse_data =  getAllHourse_infoMap()[:5]
    return render_template('detail.html',
                           username=username,
                           hourseInfo=hourseInfo
                           )

@pb.route('/addHourse', methods=['GET', 'POST'] )
def addHourse():
    username = session.get('username')
    if request.method == 'GET':
        return render_template('addHourse.html',
                           username=username,
                           )
    else:
        cover = request.files.get('cover')
        coverFilename = str(uuid.uuid4()) + '.' + cover.filename.replace('"','').split('.')[-1]
        save_path = os.path.join(app.root_path, 'static', 'hourseImg', coverFilename)
        cover.save(save_path)
        addHourseInfo({
            'title':request.form.get('title'),
            'city': request.form.get('city'),
            'region': request.form.get('region'),
            'address': request.form.get('address'),
            'rooms_desc': request.form.get('rooms_desc'),
            'area_range': request.form.get('area_range'),
            'price': request.form.get('price'),
            'hourseDecoration': request.form.get('hourseDecoration'),
            'company': request.form.get('company'),
            'hourseType': request.form.get('hourseType'),
            'tags': request.form.get('tags'),
            'cover':'http://localhost:5000/static/hourseImg/' + coverFilename
        })

        return redirect('/page/tableData')

@pb.route('/deleteHourse', methods=['GET'] )
def deleteHourse():
    id = request.args.get('id')
    deleteHourseInfo(id)
    return redirect('/page/tableData')


@pb.route('/editHourse', methods=['GET', 'POST'] )
def editHourse():
    username = session.get('username')
    if request.method == 'GET':
        id = request.args.get('id')
        hourseInfo = getHourseInfoById(id)
        return render_template('editHourse.html',
                                username=username,
                                hourseInfo=hourseInfo,

                               id=id
                           )
    else:
        id = request.args.get('id')
        cover = request.files.get('cover')
        coverFilename = str(uuid.uuid4()) + '.' + cover.filename.replace('"', '').split('.')[-1]
        save_path = os.path.join(app.root_path, 'static', 'hourseImg', coverFilename)
        cover.save(save_path)
        editHourseInfo({
                'title':request.form.get('title'),
                'city': request.form.get('city'),
                'region': request.form.get('region'),
                'address': request.form.get('address'),
                'rooms_desc': request.form.get('rooms_desc'),
                'area_range': request.form.get('area_range'),
                'price': request.form.get('price'),
                'hourseDecoration': request.form.get('hourseDecoration'),
                'company': request.form.get('company'),
                'hourseType': request.form.get('hourseType'),
                'tags': request.form.get('tags'),
                'cover':('http://localhost:5000/static/hourseImg/' + coverFilename) if request.files.get('cover') else '0'
        }, id)
        return redirect('/page/tableData')

@pb.route('/priceChar', methods=['GET', 'POST'] )
def priceChar():
    username = session.get('username')
    citiesList = getCitiesList()
    defaultCity = request.args.get('defaultCity') if request.args.get('defaultCity') else citiesList[0]
    hourseList = getAllHourse_infoMap(defaultCity)
    X,Y = getPriceCharDataOne(hourseList)
    X1,Y1 = getPriceCharDataTWo(hourseList)
    data = getPriceCharDataThree(hourseList)
    return render_template('priceChar.html',
                                username=username,
                           citiesList=citiesList,
                           defaultCity=defaultCity,
                           X=X,
                           Y=Y,
                           X1=X1,
                           Y1=Y1,
                           data = data
                           )
@pb.route('/detailChar', methods=['GET', 'POST'] )
def detailChar():
    username = session.get('username')
    hourseList = getAllHourse_infoMap()
    result = getDetailCharone(hourseList)
    defaultType = request.args.get('type') if request.args.get('type') else 'small'
    X,Y = getDetailCharTwo(hourseList,defaultType)
    return render_template('detailChar.html',
                                username=username,
                           result=result,
                           X=X,
                           Y=Y
                           )

@pb.route('/typeChar', methods=['GET', 'POST'] )
def typeChar():
    username = session.get('username')
    citiesList = getCitiesList()
    defaultCity = request.args.get('defaultCity') if request.args.get('defaultCity') else citiesList[0]
    hourseList = getAllHourse_infoMap(defaultCity)
    typeCheOneData = getTypeCharDataOne(hourseList)
    typeCheTwoData = getTypeCharDataTwo(hourseList)
    return render_template('typeChar.html',
                                username=username,
                           citiesList=citiesList,
                           defaultCity=defaultCity,
                           typeCheOneData=typeCheOneData,
                           typeCheTwoData=typeCheTwoData
                           )

@pb.route('/anotherChar', methods=['GET', 'POST'] )
def anotherChar():
    username = session.get('username')
    hourseList = getAllHourse_infoMap()
    X, Y = grtAnotherCharOne(hourseList)
    charTwoData = getAnotherCharTwo(hourseList)
    X1, Y1 = getAnotherCharThree(hourseList)
    return render_template('anotherChar.html',
                                username=username,
                           X = X, Y =  Y,
                           charTwoData = charTwoData,
                           X1 = X1, Y1 = Y1
                           )
@pb.route('/pricePred', methods=['GET', 'POST'] )
def pricePred():
    username = session.get('username')
    priceResult = 0
    if request.method == 'GET':
        citiesList = getCitiesList()
        return render_template('pricePred.html',
                               username=username,
                               citiesList=citiesList,
                               priceResult = priceResult
                               )
    else:
        # print(request.form)
        statusResult = 1
        if request.form.get('sale_status') == '在售':
            statusResult = 1
        elif request.form.get('sale_status') == '已售':
            statusResult = 2
        elif request.form.get('sale_status') == '出租中':
            statusResult = 3
        elif request.form.get('sale_status') == '已出租':
            statusResult = 4
        elif request.form.get('sale_status') == '预售':
            statusResult = 5
        elif request.form.get('sale_status') == '其他':
            statusResult = 6
        # model = index.model_train(index.getData())


