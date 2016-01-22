# -*- coding: utf-8 -*-
import json
import Queue

import arrow
from flask import Flask, request, jsonify, abort
app = Flask(__name__)
app.config['QUE'] = Queue.Queue()
app.config['IS_QUIT'] = False

@app.route('/hbc', methods=['POST'])
def hbc_post():
    if not request.json.get('carinfo', None):
        error = {
            'resource': 'hbc',
            'field': 'carinfo',
            'code': 'missing_field'
        }
        return jsonify({'message': 'Validation Failed', 'errors': error}), 422
    app.config['QUE'].put(request.json['carinfo'])
    if app.config['QUE'].qsize() >= 6:
        abort(429)
    return jsonify(), 201
