#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_login import login_required, current_user
from . import watch

@watch.route('/', methods=['GET', 'POST'])
def watchlist():
	return render_template('watch/watchlist.html')
