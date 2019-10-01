import os, json, redis
from flask import Flask, jsonify, request

# Redis
def get_redis():
  host = os.environ['REDIS_HOST']
  port = int(os.environ['REDIS_PORT'])
  db = int(os.environ['REDIS_DB'])
  return redis.Redis(host=host, port=port, db=db)
REDIS = get_redis()

# Flask
app = Flask('')

def success(d):
  return (jsonify(d), 200)

def error(code):
  message = {
    400: "Bad Request. Key and Value must be Alnum.",
    404: "Resource doesn't exist.",
    409: "Resource already exist.",
  }
  d = {'error':message[code], 'code':code}
  return (jsonify(d), code)

@app.errorhandler(404)
def internal_server_error(error):
  return html_404

@app.errorhandler(405)
def internal_server_error(error):
  d = {'error':'Method not allowed.', 'code':405}
  return (jsonify(d), 405)

@app.errorhandler(500)
def internal_server_error(error):
  d = {'error':'Server internal error.', 'code':500}
  return (jsonify(d), 500)

@app.route('/', methods=['GET'])
def page_index():
  return html_index

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
  if not key.isalnum():
    return error(400)
  if request.method in ['POST', 'PUT']:
    body = request.get_data().decode().strip()
    if not body.isalnum():
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

  fun = {'GET':get, 'POST':post, 'PUT':put, 'DELETE':delete}[request.method]
  return fun()

# Html
html_index = '''<!DOCTYPE html>
<html>
  <head>
    <title>My KVS Service</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <script>
var refreshTable = function(){
  $.ajax({type:'get', url:'/api/v1/keys/', success:function(j){
    $('#table').empty()
    var hline = '<tr><th scope="col">#</th><th scope="col">Key</th><th scope="col">Value</th></tr>'
    $('#table').append(hline)
    var index = 1
    for(var key in j){
      var line = '<tr><th scope="row">' + index + '</th><td>' + key + '</td><td>' + j[key] + '</td></tr>'
      $('#table').append(line)
      index++
    }
  }})
}
$(function(){
  $('#get-button').click(function(){
    $.ajax({type:'get', url:'/api/v1/keys/'+$('#key').val(),
      success:function(j){alert(JSON.stringify(j, null, '  '))}, 
      error:function(d){alert(d.responseText)}})
  })
  $('#post-button').click(function(){
    $.ajax({type:'post', url:'/api/v1/keys/'+$('#key').val(), data:$('#value').val(),
      success:function(d){refreshTable()}, error:function(d){alert(d.responseText)}})
  })
  $('#put-button').click(function(){
    $.ajax({type:'put', url:'/api/v1/keys/'+$('#key').val(), data:$('#value').val(),
      success:function(d){refreshTable()}, error:function(d){alert(d.responseText)}})
  })
  $('#delete-button').click(function(){
    $.ajax({type:'delete', url:'/api/v1/keys/'+$('#key').val(),
      success:function(d){refreshTable()}, error:function(d){alert(d.responseText)}})
  })
  $('#key').keyup(function(){
    $('#key-text').text('URL: /api/v1/keys/' + $('#key').val())
  })
  $('#value').keyup(function(){
    $('#value-text').text('Body: ' + $('#value').val())
  })
  refreshTable()
  setInterval(refreshTable, 5000)
})
    </script>
  </head>
  <body class="container">
    <h1 class="h3" style="padding-top:10px"><a href="/">My KVS Service</a></h1>
    <h2 class="h5" style="padding-top:20px">API呼び出し</h2>
    <div class="row">
      <div class="form-group col"><label for="key">Key(英数字のみ)</label>
        <input class="form-control" type="text" id="key"></div>
      <div class="form-group col"><label for="value">Value(英数字のみ)</label>
        <input class="form-control" type="text" id="value"></div>
    </div>
    <p id="key-text">URL: /api/v1/keys/</p>
    <p id="value-text">Body:</p>
    <p>HTTP Request: <button id="get-button" type="submit" class="btn btn-primary">GET</button>
    <button id="post-button" type="submit" class="btn btn-success">POST</button>
    <button id="put-button" type="submit" class="btn btn-warning">PUT</button>
    <button id="delete-button" type="submit" class="btn btn-danger">DELETE</button></p>
    <h2 class="h5" style="padding-top:20px">現在のKeyとValueの確認</h2>
    <table class="table" id="table"><table>
  </body>
</html>'''

html_404 = '''<!DOCTYPE html>
<html>
  <head><title>404</title>
    <script>setTimeout(function(){location.href = '/';}, 3000);</script></head>
  <body><p>404 Page Not Found</p><p>Redirecting to <a href="/">top page</a>...</p></body>
</html>'''

# Start KVS Service App
app.run(debug=False, host='0.0.0.0', port=80)
