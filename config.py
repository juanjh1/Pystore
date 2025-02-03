from flask import Flask

app = Flask(__name__, static_folder='statics')
app.secret_key = '123456789'


   
