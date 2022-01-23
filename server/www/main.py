from flask import Blueprint
from flask import render_template


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")
