import datetime

from flask import Flask, render_template,jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from Server import functesturl, updatedb, basicproxytest

e = create_engine('sqlite:///database.db')  # loads db into memory


# Resource
app = Flask(__name__, template_folder="templates")
api = Api(app)  # api is a collection of objects, where each object contains a specific functionality (GET, POST, etc)


@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

@app.route('/proxies')
def proxies():
    return render_template('proxylistview.html')

class index(Resource):
    def get(self):
        conn = e.connect()
        try:
            query = conn.execute("select * from proxyprovider")
            rows = query.cursor.fetchall()
            query_testurl = conn.execute("select * from proxytest")
            rows_testurl = query_testurl.cursor.fetchall()
            return jsonify({'tasks': rows, 'testtasks': rows_testurl})
        except:
             return {'msg': 'Error occurred ! '}, 400
        conn.close()

    def post(self):
        json = request.get_json()
        urlTest = json['url']
        conn = e.connect()

        query = conn.execute("select * from proxylists")
        rows = query.cursor.fetchall()
        if not rows:
            return {'message': 'No Proxies Are Available in the Database !'}, 400
        proxyList = []
        for i in rows:
            line = i[0]+':'+ str(i[1])
            proxyList.append(line)
        conn.close()
        functesturl(proxyList, urlTest)
        return { 'message': 'Proxy test with certain url is completed, find the details in Test URLS Division!' }, 201

class proxiesretrive(Resource):
    def get(self):
        conn = e.connect()
        try:
            query = conn.execute("select * from proxylists")
            rows = query.cursor.fetchall()
            return jsonify({'tasks': rows})
        except:
            return {'msg': 'Error occurred ! '}, 400

        conn.close()

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        conn = e.connect()
        query = conn.execute("select * from proxylists where IP = ? ", (json_data['IP']))
        row = query.cursor.fetchall()
        if not row:
            updatedb(json_data)
            return { 'message': 'IP Entry Has Been Added Successfully ' }, 201
        else:
            return { 'message': 'IP is already exists, please enter new IP address !' }, 400

        conn.close()

    def put(self):
        json_data = request.get_json()
        proxy_list = []
        if not json_data:
            return {'message': 'No input data provided'}, 400
        conn = e.connect()
        query = conn.execute("select * from proxylists where IP = ? ", (json_data['oldIP']))
        row = query.cursor.fetchall()
        if not row:
            return {'message': 'IP does not exist'}, 400
        else:
            date = str(datetime.datetime.now())
            dataformat = date[0:10] + ',' + date[11:19]
            conn.execute("UPDATE proxylists SET IP = ?, Port = ?, insertdate = ?, lastupdate = ? WHERE IP = ?",
                         (json_data['newIP'],json_data['newPort'], dataformat, dataformat, json_data['oldIP']))
            dict_line = {'IP': json_data['newIP'], 'Port': json_data['newPort']}
            proxy_list.append(dict_line)
            basicproxytest(proxy_list, dataformat)
            return {'message': 'IP Entry Has Been Updated Successfully '}, 201

        conn.close()

    def delete(self):
        json_data = request.get_json(force=True)
        if json_data == 1:
            print('deleted')
            conn = e.connect()
            conn.execute("DELETE from proxylists")
            conn.close()
            return {"status": 'success'}, 201
        else:
            return {'message': 'No input data provided'}, 400


#resource route
api.add_resource(proxiesretrive, '/proxiestest')
api.add_resource(index, '/indexpage')

if __name__ == '__main__':
    app.run(debug=True)