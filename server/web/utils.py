import os
import json

from werkzeug.utils import secure_filename

from flask import Blueprint
from flask import render_template

from .models import db
from .models import UrlModel


utils = Blueprint('utils', __name__)


@utils.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


def check_db_file(app, db, database_path):
    if os.path.exists(database_path):
        print("* DB file exist")
        return
    else:
        print("* Creating DB file")
        db.create_all(app=app)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def set_all_urls(app):
    urls = [item.path for item in UrlModel.query.all()]
    for rule in app.url_map.iter_rules():
        url = rule.rule
        if url not in urls:
            url = UrlModel(path=url)
            db.session.add(url)
            try:
                db.session.commit()
            except:
                db.session.rollback()



