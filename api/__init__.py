"""App entry point"""
from flask import Flask

application = Flask(__name__)


@application.route('/')
def index():
    """Placeholder route"""
    return 'Hello, World!'
