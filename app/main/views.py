#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import Watchlist, User, Post
from config import config
import time
import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data,
	                author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	# page = request.args.get('page', 1, type=int)
	# pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
	#     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
	#     error_out=False)
	# posts = pagination.items
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html', form=form, posts=posts)
