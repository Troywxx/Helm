from flask import Blueprint

watch = Blueprint('watch', __name__)

from . import views
