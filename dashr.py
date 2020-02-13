from flask import Flask
from flask_redis import FlaskRedis


REDIS_URL = "redis://:password@localhost:6379/0"


app = Flask(__name__)
redis_client = FlaskRedis(app)


@app.route('/', methods=['GET'])
def want_some_rest():
    return "Want some rest?"


@app.route('/potero', methods=['GET'])
def potero():
    return str(redis_client.get('potato'))


@app.route('/potaro', methods=['GET'])
def potaro():
    redis_client.setex('potato', 10, 'test')
    return 'Done'


if __name__ == '__main__':
    app.run(debug=True)
