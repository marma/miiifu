#!/usr/bin/env python3

from io import BytesIO
from flask import Flask,request,render_template,Response,redirect,url_for
from flask_caching import Cache
from yaml import load as yload,FullLoader
from os.path import exists,join
from json import dumps,loads
from iiif import get_region, get_size
from resolve import resolve_identifier
from utils import HttpException

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)
config = yload(open(join(app.root_path, 'config.yml')).read(), Loader=FullLoader)

mimes = {
    'jpg': 'image/jpeg',
    'tif': 'image/tiff',
    'jp2': 'image/jpeg2000',
    'png': 'image/png'
}

@app.route('/iiif/<identifier>/<region>/<size>/<float:rotation>/<quality>.<fmt>')
def iiif_image(identifier, region, size, rotation, quality, fmt):
    try:
        validate(region, size, rotation, quality, fmt)
        path = resolve(identifier)
        info = get_info(path)

        if info:
            return Response(
                    export(
                        convert(
                            info,
                            path,
                            region,
                            size),
                        quality,
                        fmt),
                    mime_type(mimes[fmt]))

        return 'Not found', 404
    except HttpException as e:
        return str(e), e.status_code


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


def export(im, quality, fmt):
    b = BytesIO()
    im.save(b, quality=90, progressive=True, format='jpeg')

    return b.getvalue()

