from flask import Flask, request, jsonify, make_response, render_template
import jwt
import datetime
import os
from flask_cors import CORS, cross_origin
from flask_caching import Cache

app = Flask(__name__)
CORS(app,vary_header=False,send_wildcard=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
# Endpoint to generate JWT token
@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Missing username or password', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    # check if the provided credentials are valid
    if auth['username'] != 'admin' or auth['password'] != 'password':
        return make_response('Could not verify username and password', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    # generate and encode JWT token
    token = jwt.encode({'username': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    
    # Set the token in localstorage
    response = jsonify({'access_token': token})
    response.status_code = 200
    response.headers['Authorization'] = 'Bearer {}'.format(token)
    response.headers['Access-Control-Expose-Headers'] = 'Authorization'
    #response.set_cookie('username', 'John Doe')
    return response



# Protected endpoint that requires JWT token

@app.route('/protected', methods =['GET'])
#@cross_origin(origins='*',supports_credentials='True')
@cache.cached(timeout=600)
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return make_response('Authorization header missing', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    try:
        decoded_token = jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return make_response('Signature expired. Please log in again.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    except jwt.InvalidTokenError:
        return make_response('Invalid token. Please log in again.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    return 'Welcome, {}! Your API Key : sakeowdskdsjkdksdks'.format(decoded_token['username'])

if __name__ == '__main__':
    app.run()
