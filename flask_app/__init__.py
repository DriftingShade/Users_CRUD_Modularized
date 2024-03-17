from flask import Flask
from flask import session

app = Flask(__name__)
app.secret_key = "It's a Secret, Bro"
