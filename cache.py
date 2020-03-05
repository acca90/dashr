from flask import Flask, jsonify
from flask_caching import Cache
from flask_mysqldb import MySQL

config = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 100,
    'CACHE_KEY_PREFIX': 'H0K0_',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    # 'CACHE_REDIS_PASSWORD': '',
    'CACHE_REDIS_DB': 0,
    # 'CACHE_OPTIONS': '',
}

# config = {
#     'CACHE_TYPE': 'redis',
#     'CACHE_DEFAULT_TIMEOUT': 10,
#     'CACHE_KEY_PREFIX': 'H0K0_',
#     'CACHE_REDIS_HOST': '167.99.91.111',
#     'CACHE_REDIS_PORT': '6379',
#     'CACHE_REDIS_PASSWORD': 'thispasswordissecure',
#     'CACHE_REDIS_DB': 0,
#     # 'CACHE_OPTIONS': '',
# }

app = Flask(__name__)
mysql = MySQL()
cache = Cache(config=config)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rfgejgyso1XQ3'
app.config['MYSQL_DB'] = 'cache_this'
mysql.init_app(app)
cache.init_app(app)


@cache.cached(100, key_prefix='WALLET_')
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

    return jsonify(json_data)


@app.route('/cache', methods=['GET'])
def get_all_wallets():
    return base_query()


if __name__ == '__main__':
    app.run(debug=True)
