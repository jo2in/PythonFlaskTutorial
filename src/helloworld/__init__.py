from flask import Flask
from helloworld.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from helloworld import routes
