from pymysql import  *

conn = connect(host='localhost', user='root', password='041219', database='hourses_data', port=3306)
cursor = conn.cursor()

def querys(sql, params, type='no_select'):
    params = tuple(params)
    cursor.execute(sql, params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()