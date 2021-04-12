from flask import Flask

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'secret_key'

from app import routes
