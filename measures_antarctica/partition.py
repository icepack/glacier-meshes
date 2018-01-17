
import numpy as np
import netCDF4
import geojson
import math
from icepack.grid import arcinfo, GridData

def main():
    # Read the velocity maps into two `GridData` objects
    with netCDF4.Dataset("antarctica_ice_velocity_900m.nc", 'r') as velocity:
        nx, ny = velocity.nx, velocity.ny
        xmin, ymax = float(velocity.xmin[:-1]), float(velocity.ymax[:-1])
        dx = float(velocity.spacing[:-1])

        x = np.linspace(xmin, xmin + nx * dx, nx, False)
        y = np.linspace(ymax - ny * dx, ymax, ny, False)

        # The data in the NetCDF file are stored upside-down in the `y`-
        # direction making everything very confusing.
        err = velocity['err'][::-1,:]

        # An error value of 0.0 indicates missing data
        mask = (err == 0.0)

        vx = GridData(x, y, velocity['vx'][::-1,:], mask=mask)
        vy = GridData(x, y, velocity['vy'][::-1,:], mask=mask)

    # Get a list of interesting regions in Antarctica
    with open("../regions/antarctica.geojson", "r") as geojson_file:
        regions = geojson.loads(geojson_file.read())

    # Save a section of the velocity map for each region to separate files
    for region in regions['features']:
        region_name = region['properties']['name'].lower()
        bounding_box = region['geometry']['coordinates']

        xmin, ymin = bounding_box[0]
        xmax, ymax = bounding_box[1]

        with open(region_name + "-vx.txt", 'w') as region_vx:
            arcinfo.write(region_vx, vx.subset(xmin, ymin, xmax, ymax), -2e9)

        with open(region_name + "-vy.txt", 'w') as region_vy:
            arcinfo.write(region_vy, vy.subset(xmin, ymin, xmax, ymax), -2e9)


if __name__ == "__main__":
    main()

