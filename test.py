from iiif import region_coords,scale_dimensions

info = { 'width': 1024, 'height': 1024 }

assert(region_coords(info, 'full') == (0, 0, info['width'], info['height']))
assert(region_coords(info, '512,512,512,512') == (512,512,512,512))
assert(region_coords(info, '512,512,1024,1024') == (512,512,512,512))

assert(scale_dimensions(info, region_coords(info, 'full'), 'max') == (info['width'], info['height']))
assert(scale_dimensions(info, region_coords(info, '512,512,512,512'), '256,') == (256,256))

#print(region_coords(info, '0,0,1024,512'))
#print(scale_dimensions(info, region_coords(info, '0,0,1024,512'), '256,'))
assert(scale_dimensions(info, region_coords(info, '0,0,1024,512'), '256,') == (256, 128))


