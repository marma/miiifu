from subprocess import run
from iiif import region_coords, scale_dimensions
from subprocess import run,PIPE,DEVNULL
from logging import debug,info as log_info,warning,error
from math import log2
from tempfile import NamedTemporaryFile
from utils import HttpException
from PIL import Image,ImageFilter
from time import time
import logging

logging.basicConfig(level=logging.INFO)

def convert(info, path, region, size):
    if info['format'] == 'JPEG2000':
        return cropscale_j2k(info, path, region, size)

    raise HttpException(f'Format not supported ({info.get("format")})', 400)


def cropscale_j2k(info, path, region, scale, oversample=False):
    # TODO: make command configurable
    decompress_command = '/usr/bin/grk_decompress'
    ow,oh = info['width'], info['height']
    x,y,w,h = region_coords(info, region)
    sw,sh = scale_dimensions(info, (x,y,w,h), scale)

    # calculate reduce factor based on original width and scaled width
    # ignore non-proportional scaling for now
    reduce_factor = int(log2(w/sw))

    # Use larger image to get better quality?
    if oversample:
        reduce_factor = max(0, reduce_factor-1)

    # run decompress
    with NamedTemporaryFile(suffix='.tif') as t:
        cmd = f'{decompress_command} -V -r {reduce_factor} -d {x},{y},{x+w},{y+h} -i {path} -o {t.name}'
        log_info(cmd)

        t0=time()
        ret = run(cmd.split(), text=True, stderr=PIPE, stdout=DEVNULL)
        t1=time()
        log_info(f'grk_decompress took {int(1000*(t1-t0))}ms')

        if ret.returncode != 0:
            error(' '.join(cmd))
            error(f'{decompress_command} returned {ret.returncode}')
            error(ret.stderr)

            raise HttpException('Error while decoding JPEG2000', 500)

        with Image.open(t.name) as im:
            im.load()

    scale_factors = (sw/w, sh/h)
    im = im.resize((sw, sh), resample=Image.LANCZOS)
    im = im.convert('RGB')

    # sharpen?
    if scale_factors[0] < 1.0 or scale_factors[1] < 1.0:
        im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=90, threshold=3))

    return im


