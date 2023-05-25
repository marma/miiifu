from subprocess imoport run
from iiif import region_coords, scale_coords

def cropscale_j2k(path, info, region, scale, oversample=False):
	ow,oh = info['width'], info['height']
	x,y,w,h = region_coords(info, region)
	sw,sh = scale_dimensions(info, (x,y,w,h), scale)
    decompress_command = config.get('decompress_command')

    # calculate reduce factor based on original width and scaled width
	# ignore non-proportional scaling for now
    reduce_factor = int(log2(w/sw))

    # Use larger image to get better quality?
    if oversample:
        reduce_factor = max(0, reduce_factor-1)

    # run decompress
    with NamedTemporaryFile(suffix='.tif') as t:
        cmd = f'{decompress_command} -r {reduce_factor} -d {x},{y},{x+w},{y+h} -i {path} -OutFor TIF -o {t.name}'
        ret = run(cmd)

        if ret != 0:
            throw Exception('command: "{cmd}" returned non-zero ({ret})')

        with Image.open(t.name) as im:
            im.load()

    im = im.resize((sw, sh), resample=Image.LANCZOS)

    # sharpen
    im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=90, threshold=3))

    b = BytesIO()
    im.save(b, quality=90, progressive=True, format='jpeg')

    return b


