import pandas as pd
from sqlalchemy import create_engine
from  sklearn.preprocessing import LabelEncoder
from  sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import json
conn = create_engine('mysql+pymysql://root:041219@localhost:3306/hourses_data?charset=utf8')
transfer = LabelEncoder()

def getData():
    df = pd.read_sql('select * from hourse_info',con=conn, index_col='id')
    X = df[['city', 'rooms_desc', 'area_range', 'hourseType', 'sale_status', 'price']]
    X['hourseType'] = X['hourseType'].replace('住宅', 0)\
    .replace('别墅', 1)\
    .replace('商业类', 2)\
    .replace('商业', 3)\
    .replace('酒店式公寓', 4)\
    .replace('底商', 5)\
    .replace('写字楼', 6)\
    .replace('车库', 7)


if __name__ == '__main__':
    getData()