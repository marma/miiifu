#!/usr/bin/env python3

from flask import Flask,request,render_template,Response,redirect,url_for
from flask_caching import Cache
from yaml import load as yload,FullLoader
from os.path import exists,join
from json import dumps,loads
from iiif import get_region, get_size
from resolve import resolve_identifier
from subroutine import run
from j2k import cropscale_j2k

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)
config = {}

@app.route('/iiif/<identifier>/<region>/<size>/<float:rotation>/<quality>.<fmt>')
def iiif_image(identifier, region, size, rotation, quality, fmt):
    try:
        validate(region, size, rotation, quality, fmt)
    except Exception as e:
        return str(e), 400

    path = resolve(identifier)
    info = get_info(path)
    if info:
        if info['format'] == 'JPEG2000':
            b = cropscale_j2k(info, path, region, size)

            return Response(b, mime_type='image/jpeg')
        else:
            return f'Format not supported ({info.get("format")})', 400

    return 'Not found', 404


@app.route('/iiif/<identifier>/info.json')
def iiif_info(identifier):
    path = resolve(identifier)
    info = get_info(path)

    if info:
        return render_template('info.json', **info, mime_type='application/json')

	return 'Not found', 404


@cache.cached()
def get_info(path):
	if exists(path):
        with Image.open(path) as i:
    	    return { 'format': i.format, 'width': i.width, 'height': i.height }

	return None


@cache.cached()
def resolve(identifier):
    return resolve_identifier(identifier, config.get('resolve', {})

