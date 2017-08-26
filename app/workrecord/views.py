#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user
from . import workrecord
from .forms import PostForm
from .. import db
from ..models import Watchlist, User, Post
from config import config
import time
import datetime


@workrecord.route('/', methods=['GET', 'POST'])
def record_handler():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data,
	                worktype=form.worktype.data,
	                event_starttime=form.event_starttime.data,
	                author=current_user._get_current_object(),
	                )
		db.session.add(post)
		return redirect(url_for('.record_handler'))
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
	    page, per_page=20,
	    error_out=False)
	posts = pagination.items
	return render_template('workrecord/workrecord.html', form=form, posts=posts, pagination=pagination)
