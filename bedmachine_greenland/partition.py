
import numpy as np
import netCDF4
import geojson
from icepack.grid import arcinfo, GridData

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
        region_name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        with open(region_name + "-bed.txt", 'w') as region_bed:
            arcinfo.write(region_bed, bed.subset(box[0], box[1]), -2e9)

        with open(region_name + "-surface.txt", 'w') as region_surface:
            arcinfo.write(region_surface, surface.subset(box[0], box[1]), -2e9)

if __name__ == "__main__":
    main()
