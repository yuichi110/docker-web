import os, json, re, redis
from flask import Flask, jsonify, request

###
### Connection to Redis
###

def get_redis():
  host = os.environ['REDIS_HOST']
  port = int(os.environ['REDIS_PORT'])
  db = int(os.environ['REDIS_DB'])
  return redis.Redis(host=host, port=port, db=db)

REDIS = get_redis()


###
### Flask
###

app = Flask('')

# API

@app.route('/api/v1/keys/', methods=['GET'])
def api_keys():
  data = {}
  cursor = '0'
  while cursor != 0:
    cursor, keys = REDIS.scan(cursor=cursor, count=1000000)
    if len(keys) == 0:
      break
    keys = [key.decode() for key in keys]
    values = [value.decode() for value in REDIS.mget(*keys)]
    data.update(dict(zip(keys, values)))
  return success(data)

@app.route('/api/v1/keys/<key>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_key(key):
  if not isalnum(key):
    return error(400)
  if request.method in ['POST', 'PUT']:
    body = request.get_data().decode().strip()
    if not isalnum(body):
      return error(400)

  def get():
    value = REDIS.get(key)
    if value is not None:
      return success({key:value.decode()})
    return error(404)
  def post():
    if REDIS.get(key) is not None:
      return error(409)
    REDIS.set(key, body)
    return success({key:body})
  def put():
    REDIS.set(key, body)
    return success({key:body})
  def delete():
    if REDIS.delete(key) == 0:
      return error(404)
    return success({})

  fdict = {'GET':get, 'POST':post, 'PUT':put, 'DELETE':delete}
  return fdict[request.method]()

# Utility

_alnum_pat = re.compile(r'^[a-zA-Z0-9]+$')
def isalnum(text):
  return _alnum_pat.match(text) is not None

def success(d):
  return (jsonify(d), 200)

def error(code):
  message = {
    400: "Bad Request. Key(URL) and Value(Body) must be Alnum",
    404: "Resource not found",
    409: "Conflict. Resource already exist",
  }
  d = {'error':message[code], 'code':code}
  return (jsonify(d), code)

# Error Handling

@app.errorhandler(404)
def api_not_found_error(error):
  d = {'error':"API not found", 'code':404}
  return (jsonify(d), 404)

@app.errorhandler(405)
def method_not_allowed_error(error):
  d = {'error':'Method not allowed', 'code':405}
  return (jsonify(d), 405)

@app.errorhandler(500)
def internal_server_error(error):
  d = {'error':'Server internal error', 'code':500}
  return (jsonify(d), 500)


# Start

app.run(debug=False, host='0.0.0.0', port=80)
