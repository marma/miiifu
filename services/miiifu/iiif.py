from utils import HttpException

# TODO: rewrite
def region_coords(info, region):
    width = info['width']
    height = info['height']

    if region != 'full':
        if region == 'square':
            diff = abs(width - height)
            if width > height:
                x,y,w,h = diff/2, 0, height, height
            else:
                x,y,w,h = 0, diff/2, width, width
        elif region[:4] == 'pct:':
            z = [ width, height, width, height ]
            s = [ int(z[x[0]]*float(x[1])) for x in enumerate(region[4:].split(',')) ]
            x,y,w,h = s[0], s[1], min(s[2], width), min(s[3], height)
        else:
            s = [ int(x) for x in region.split(',') ]
            x,y,w,h = s[0], s[1], min(s[2], width-s[0]), min(s[3], height-s[1])

        return (x,y,w,h)
    else:
        return (0,0,width, height)


# TODO: rewrite
def scale_dimensions(info, region_coords, scale, tile_size=None):
    width = region_coords[2] # info['width']
    height = region_coords[3] # info['height']
    max_resize = 2048

    if scale not in [ 'full', 'max' ]:
        if scale[:4] == 'pct:':
            s = float(scale[4:])/100
            if s <= 1.0:
                w,h = int(width*s), int(height*s)
        elif scale[0] == '!':
            s = scale[1:].split(',')

            if s[0] == '':
                s[1] = min(int(s[1]), width)
                w,h = int(width * s[1] / height), s[1]
            elif s[1] == '':
                s[0] = min(int(s[0]), width)
                w,h = s[0], int(height * s[0] / width)
            else:
                s = [ min(int(s[0]), width), min(int(s[1]), height) ]
                w,h = s[0], s[1]

            if width > height:
                h = int(w * height / width)
            else:
                w = int(h * width / height)
        else:
            s = scale.split(',')

            if s[0] == '':
                s[1] = int(s[1])
                w,h = int(width * s[1] / height), s[1]
            elif s[1] == '':
                s[0] = int(s[0])
                w,h = s[0], int(height * s[0] / width)

                # correct for rounding errors?
                h1 = int(height * (s[0]-1) / width)
                if tile_size and h > tile_size and h1 <= tile_size:
                    h = tile_size
            else:
                #s = [ min(int(s[0]), image.width), min(int(s[1]), image.height) ]
                w,h = int(s[0]), int(s[1])
    else:
        w,h = width, height

    if w > max_resize or h > max_resize:
        raise HttpException(f'width ({w}) or height ({h}) larger than max resize limit ({max_resize})', 400)
        
    return (w, h)

