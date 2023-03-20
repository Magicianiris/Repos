# pip install pymssql

import pymssql


server = '117.80.119.37:52515'
user = 'sa'
password = 'P)P)PUOIYqeyue6ui'
database = 'UFDATA_181_2014'


def execute(sql):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql)


def get_data(sql):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data[0][0]


def get_datatable(sql):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def create_map(keys):
    map = {}
    i = 0
    for i in range(len(keys)):
        map.update({keys[i]: i})
    return map


def connect():
    return pymssql.connect(server, user, password, database, charset="UTF-8")
