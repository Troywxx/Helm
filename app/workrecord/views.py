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


@workrecord.route('/addrecord', methods=['GET','POST'])
def add_record():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.body.data,
	                worktype=form.worktype.data,
	                worktag=form.worktag.data,
	                event_starttime=datetime.datetime.combine(datetime.datetime.utcnow() , form.event_starttime.data.time()),
	                event_endtime=datetime.datetime.combine(datetime.datetime.utcnow() , form.event_endtime.data.time()),
	                author=current_user._get_current_object(),
	                )
		db.session.add(post)
		return redirect(url_for('.show_record'))
	return render_template('workrecord/add_record.html', form=form)

@workrecord.route('/showrecord', methods=['GET'])
def show_record():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
	    page, per_page=20,
	    error_out=False)
	posts = pagination.items
	return render_template('workrecord/show_record.html', posts=posts, pagination=pagination)

@workrecord.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_record(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_m = Post(body=form.body.data,
        			worktype=form.worktype.data,
	                worktag=form.worktag.data,
	                event_starttime=datetime.datetime.combine(datetime.datetime.utcnow() , form.event_starttime.data.time()),
	                event_endtime=datetime.datetime.combine(datetime.datetime.utcnow() , form.event_endtime.data.time()),
                    author=current_user._get_current_object())
        db.session.add(post_m)
        db.session.commit()
        post.modify_count += 1
        post.show_ack = False
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.show_record'))
    form.body.data = post.body
    return render_template('workrecord/edit_record.html', form=form)

@workrecord.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_record(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
            abort(403)
    post.show_ack = False
    post.deleted = True
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('.show_record'))