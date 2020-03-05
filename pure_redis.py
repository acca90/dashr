import json

from flask import Flask, jsonify
from flask_mysqldb import MySQL
import redis

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rfgejgyso1XQ3'
app.config['MYSQL_DB'] = 'cache_this'
mysql.init_app(app)

REDIS_URL = "redis://:password@localhost:6379/0"


redis = redis.Redis()


def base_query():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute(
        'select '
        '   field02, '
        '   CONVERT(field03, char(200)) as field03, '
        '   CONVERT(field04, char(200)) as field04, '
        '   CONVERT(field05, char(200)) as field05, '
        '   CONVERT(field06, char(200)) as field06, '
        '   field07, '
        '   field08, '
        '   field09, '
        '   field10 '
        ' from '
        '   prety_large_table'
        ' limit 10000;'
    )
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    conn.close()

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return json_data


def redis_store(user):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute(
        'select '
        '   field02, '
        '   CONVERT(field03, char(200)) as field03, '
        '   CONVERT(field04, char(200)) as field04, '
        '   CONVERT(field05, char(200)) as field05, '
        '   CONVERT(field06, char(200)) as field06, '
        '   field07, '
        '   field08, '
        '   field09, '
        '   field10 '
        ' from '
        '   prety_large_table'
        ' limit 10000;'
    )
    row_headers = [x[0] for x in cursor.description]
    rv = cursor.fetchall()
    conn.close()

    json_data = []
    row = 0
    for result in rv:
        key = 'KEY_' + user + '_' + str(row)
        redis.execute_command('JSON.DEL', key)
        row += 1

    return json_data


@app.route('/plain/<string:user>', methods=['GET'])
def plain(user):
    redis_store(user)
    return 'aaa'


@app.route('/bad_approach', methods=['GET'])
def want_some_rest():
    test = redis.execute_command('JSON.GET', 'test')

    if test is None:
        query = base_query()
        redis.execute_command('JSON.SET', 'test', '.', json.dumps(query))
        print('stored')
        return jsonify(query)

    else:
        print('cached')
        return jsonify(json.loads(test))


if __name__ == '__main__':
    app.run(debug=True)
