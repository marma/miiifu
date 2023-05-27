#!/usr/bin/env python3

from io import BytesIO
from flask import Flask,request,render_template,Response,redirect,url_for
from flask_caching import Cache
from werkzeug.security import safe_join
from yaml import load as yload,FullLoader
from os.path import exists,join
from json import dumps,loads
from iiif import region_coords, scale_dimensions
from resolve import resolve_identifier
from utils import HttpException,RegexConverter
from logging import debug,info,warning,error
from validate import validate
from convert import convert
from PIL import Image

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(__name__)
cache.init_app(app)
config = yload(open(join(app.root_path, 'config.yml')).read(), Loader=FullLoader)
app.url_map.converters['regex'] = RegexConverter

mimes = {
    'jpg': 'image/jpeg',
    'tif': 'image/tiff',
    'jp2': 'image/jpeg2000',
    'png': 'image/png'
}

@app.route('/iiif/<identifier>/<region>/<size>/<rotation>/<regex("default"):quality>.<fmt>')
def iiif_image(identifier, region, size, rotation, quality, fmt):
    try:
        validate(region, size, rotation, quality, fmt)
        path = resolve(identifier)
        info = get_info(path)

        if info:
            return Response(
                    export(
                        info,
                        convert(
                            info,
                            path,
                            region,
                            size),
                        quality,
                        fmt),
                    mimetype=mimes[fmt])

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


@cache.memoize()
def get_info(path):
    if exists(path):
        with Image.open(path) as i:
            return { 'format': i.format, 'width': i.width, 'height': i.height, 'icc_profile': i.info.get("icc_profile", None) }

    return None


@cache.memoize()
def resolve(identifier):
    assert('path_prefix' in config)
    assert(config.get('path_prefix') not in [ '/', '.', '..' ])

    return safe_join(
                config.get('path_prefix'),
                resolve_identifier(
                    identifier,
                    config.get('resolve', {})))


def export(info, im, quality, fmt):
    b = BytesIO()
    icc_profile = im.info.get("icc_profile", None)

    im.save(
        b,
        icc_profile=icc_profile,
        quality=90,
        progressive=True,
        format='jpeg' if fmt == 'jpg' else fmt)

    return b.getvalue()

