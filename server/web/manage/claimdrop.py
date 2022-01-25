from flask import Blueprint

from flask import request
from flask import url_for
from flask import render_template
from flask import current_app


claimdrop = Blueprint('api', __name__)


@claimdrop.route("/claimdrop")
def claimdrop_view():

    return render_template("manage/claimdrop.html")