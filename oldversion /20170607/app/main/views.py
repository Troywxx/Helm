#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from . import main
from .. import db
from ..watcher import Product
from ..models import Watchlist
from config import config
import time
import datetime


@main.route('/', methods=['GET', 'POST'])
def index():

    BJT_today = time.strftime("%Y %b %d")
    time_utc = datetime.datetime.utcnow().strftime("%H:%M:%S")
    time_bjt = datetime.datetime.now().strftime("%H:%M:%S")

    products = config['products']
    for key in products:
        prd_config = products[key]
        prd_ins = Product(products[key])
        prd = prd_ins.login()
        prd_ins.listen()
        
        prd_list_type = prd_config["prd_type"]
        prd_list = Watchlist(prd_type=prd_list_type,inserttime=prd[0], alert=prd[1], filename=prd[2], filetime=prd[3])
        db.session.add(prd_list)
        db.session.commit()

    radar = Watchlist.query.order_by(Watchlist.id.desc()).filter_by(prd_type='radar').first()
    awos = Watchlist.query.order_by(Watchlist.id.desc()).filter_by(prd_type='awos').first()
    sat = Watchlist.query.order_by(Watchlist.id.desc()).filter_by(prd_type='satellite').first()

    return render_template('index.html', BJT_today=BJT_today, time_utc=time_utc, time_bjt=time_bjt, radar=radar, awos=awos, sat=sat)
