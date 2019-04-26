import numpy as np
import netCDF4
import geojson
from icepack.grid import geotiff, GridData

def main():
    with netCDF4.Dataset("BedMachineGreenland-2017-09-20.nc", 'r') as dem:
        nx, ny = len(dem['x']), len(dem['y'])
        xmin, ymax = dem.xmin, dem.ymax
        dx = dem.spacing

        mask = dem['mask'][::-1,:]
        mask = np.logical_or(mask == 0, mask == 4)

        bed = GridData((xmin, ymax - ny * dx), dx, dem['bed'][::-1,:],
                       missing_data_value=-9999)
        surface = GridData((xmin, ymax - ny * dx), dx, dem['surface'][::-1,:],
                           mask=mask)

    with open("../regions/greenland.geojson", 'r') as geojson_file:
        regions = geojson.loads(geojson_file.read())

    for region in regions['features']:
        name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        geotiff.write(name + '-bed.tif', bed.subset(box[0], box[1]),
                      missing=-2e9, crs='epsg:3413')
        geotiff.write(name + '-surface.tif', surface.subset(box[0], box[1]),
                      missing=-2e9, crs='epsg:3413')

if __name__ == "__main__":
    main()
