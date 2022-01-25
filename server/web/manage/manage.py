from flask import Blueprint

from flask import request
from flask import url_for
from flask import redirect


manage = Blueprint('manage', __name__, url_prefix="/manage")