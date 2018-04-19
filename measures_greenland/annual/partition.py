
import geojson
from icepack.grid import arcinfo, geotiff

def main():
    vx = geotiff.read("greenland_vel_mosaic200_2015_vx_v01.tif")
    vy = geotiff.read("greenland_vel_mosaic200_2015_vy_v01.tif")

    with open("../../regions/greenland.geojson", 'r') as geojson_file:
        regions = geojson.loads(geojson_file.read())

    for region in regions['features']:
        region_name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        arcinfo.write(region_name + "-vx.txt", vx.subset(box[0], box[1]), -2e9)
        arcinfo.write(region_name + "-vy.txt", vy.subset(box[0], box[1]), -2e9)

if __name__ == "__main__":
    main()
