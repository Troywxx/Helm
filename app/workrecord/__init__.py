from flask import Blueprint

workrecord = Blueprint('workrecord', __name__)

from . import views
