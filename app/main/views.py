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

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_m = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post_m)
        db.session.commit()
        post.modify_count += 1
        post.show_ack = False
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('main.index'))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
            abort(403)
    post.show_ack = False
    post.deleted = True
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('main.index'))