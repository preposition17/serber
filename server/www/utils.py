import os
import json

from werkzeug.utils import secure_filename

from flask import Blueprint
from flask import render_template


utils = Blueprint('utils', __name__)


@utils.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404
