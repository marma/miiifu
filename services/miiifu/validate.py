from re import match

valid_region = r'full|[0-9]+,[0-9]+,[0-9]+,[0-9]'
valid_scale = r'max|full|[!^]?([0-9]*,[0-9]+|[0-9]+,[0-9]*)'

def validate(region, scale, rotation, quality, fmt):
    validate_region(region)
    validate_scale(scale)
    validate_rotation(rotation)
    validate_quality(quality)
    validate_format(fmt)


def validate_region(region):
    if not match(valid_region, region):
        raise Exception(f'')


def validate_scale(scale):
    if not match(valid_scale, scale):
        raise Exception(f'')


def validate_rotation(rotation):
    if float(rotation) != 0.0:
        raise Exception(f'')


def validate_quality(quality):
    if quality != 'default':
        raise Exception(f'')


def validate_format(fmt):
    if fmt not in [ 'jpg', 'png' ]:
        raise Exception(f'')

