from flask import jsonify, request, current_app, url_for, json
from flask_login import login_required, current_user
from . import api
from ..models import User, Post, Permission
from .. import db
import datetime
import time

@api.route('/postlist/<int:id>/delete/', methods=['POST'])
def postlist_delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
            abort(403)
    db.session.delete(post)
    db.session.commit()
    return "Deleted"