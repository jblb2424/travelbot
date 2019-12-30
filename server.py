from os import environ
from flask import Flask

app = Flask(__name__)
app.run(int(os.environ.get('PORT', 33507)))