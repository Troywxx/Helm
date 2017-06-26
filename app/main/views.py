#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from . import main
from .. import db
from ..models import Watchlist
from config import config
import time
import datetime


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')
