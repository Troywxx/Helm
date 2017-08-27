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
	posts = Post.query.filter_by(show_ack=True).order_by(Post.timestamp.desc()).all()
	return render_template('index.html', posts=posts)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.filter_by(show_ack=True).order_by(Post.timestamp.desc()).paginate(
        page, per_page=20,
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)
