# pip install gevent
# pip install flask

import json
import sql as Sql

from gevent import pywsgi
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/get_months', methods=['post'])
@cross_origin()
def get_months():
    sql = "select cmonth from MT_ComputeState order by cmonth desc"
    map = Sql.create_map(["cmonth"])
    print(sql)
    datatable = Sql.get_datatable(sql)
    months = []
    for row in datatable:
        months.append(row[map["cmonth"]])

    response = months
    print(response)
    return json.dumps(response)


@app.route('/get_caled', methods=['post'])
@cross_origin()
def get_caled():
    params = request.json
    month = params.get("month")

    sql = "select cstate from MT_ComputeState where cmonth = '"+str(month)+"'"
    print(sql)
    data = Sql.get_data(sql)

    response = {"status": data}
    print(response)
    return json.dumps(response)


@app.route('/get_query_codes', methods=['post'])
@cross_origin()
def get_query_codes():
    sql = "select distinct f_cquerycode from MT_SaleDataSet order by f_cquerycode"
    map = Sql.create_map(["f_cquerycode"])
    print(sql)
    datatable = Sql.get_datatable(sql)
    query_codes = []
    for row in datatable:
        query_codes.append(row[map["f_cquerycode"]])

    response = query_codes
    print(response)
    return json.dumps(response)


@app.route('/get_query_data', methods=['post'])
@cross_origin()
def get_query_data():
    params = request.json
    month = params.get("month")
    query_code = params.get("query_code")

    cols = []
    cols_show = []

    sql_cols = "exec Cust_Proc_SalesCostRecalculation_cols '"+str(month)+"','"+str(query_code)+"'"
    map_cols = Sql.create_map(["code","name"])
    datatable_cols = Sql.get_datatable(sql_cols)
    for row in datatable_cols:
        cols.append(str(row[map_cols["code"]]))
        cols_show.append(str(row[map_cols["name"]]))

    sql_values = "exec Cust_Proc_SalesCostRecalculation_values '"+str(month)+"','"+str(query_code)+"'"
    print(sql_values)
    datatable_values = Sql.get_datatable(sql_values)
    table = []
    for row in datatable_values:
        values = []
        for i in range(len(cols)):
            value=str(row[i])
            if value=="None":
                value=""
            values.append(value)
        table.append(dict(zip(cols_show, values)))

    response = table
    return json.dumps(response)

@app.route('/get_query_cols', methods=['post'])
@cross_origin()
def get_query_cols():
    params = request.json
    month = params.get("month")
    query_code = params.get("query_code")

    cols_show = []

    sql_cols = "exec Cust_Proc_SalesCostRecalculation_cols '"+str(month)+"','"+str(query_code)+"'"
    map_cols = Sql.create_map(["code","name"])
    datatable_cols = Sql.get_datatable(sql_cols)
    for row in datatable_cols:
        cols_show.append(str(row[map_cols["name"]]))

    response = cols_show
    return json.dumps(response)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8085, debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 8085), app)
    server.serve_forever()
