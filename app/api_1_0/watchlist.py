from flask import jsonify, request, current_app, url_for, json
from . import api
from ..models import Watchlist
from .. import db
import datetime
import time


@api.route('/watchlist/<prd_type>/get/')
def get_list(prd_type):
	query = Watchlist.query.order_by(Watchlist.id.desc())
	result = query.filter_by(prd_type=prd_type).first()
	result_json = {
		'Prd_Type':result.prd_type,
		'Inserttime':result.inserttime,
		'Alert':result.alert,
		'Filename':result.filename,
		'Filetime':result.filetime.strftime("%Y-%m-%d %H:%M:%S")
	}
	return jsonify(result_json)

@api.route('/watchlist/<watchlist>/write/', methods=['POST'])
def write_list(watchlist):
	data = json.loads(request.get_data())
	data['filetime'] = datetime.datetime.fromtimestamp(data['filetime'])
	print data['filetime']
	prd_list = Watchlist(prd_type=data['prd_type'], alert=data['alert'], filename=data['filename'], filetime=data['filetime'])
	db.session.add(prd_list)
	db.session.commit()
	return "OK"
