import geojson
from icepack.grid import geotiff

def main():
    vx = geotiff.read("greenland_vel_mosaic200_2015_vx_v01.tif")
    vy = geotiff.read("greenland_vel_mosaic200_2015_vy_v01.tif")
    ex = geotiff.read("greenland_vel_mosaic200_2015_ex_v01.tif")
    ey = geotiff.read("greenland_vel_mosaic200_2015_ey_v01.tif")

    with open('../../regions/greenland.geojson', 'r') as geojson_file:
        regions = geojson.loads(geojson_file.read())

    crs = 'epsg:3413'
    for region in regions['features']:
        name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        geotiff.write(name + '-vx.tif', vx.subset(*box), missing=-2e9, crs=crs)
        geotiff.write(name + '-vy.tif', vy.subset(*box), missing=-2e9, crs=crs)
        geotiff.write(name + '-ex.tif', ex.subset(*box), missing=-2e9, crs=crs)
        geotiff.write(name + '-ey.tif', ey.subset(*box), missing=-2e9, crs=crs)

if __name__ == '__main__':
    main()
