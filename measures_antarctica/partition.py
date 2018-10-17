import os.path
import numpy as np
import netCDF4
import geojson
from icepack.grid import arcinfo, GridData

def main():
    # Get a list of interesting regions in Antarctica
    with open("../regions/antarctica.geojson", "r") as geojson_file:
        regions = geojson.loads(geojson_file.read())

    # Read the velocity maps into two `GridData` objects
    with netCDF4.Dataset("antarctica_ice_velocity_450m_v2.nc", 'r') as velocity:
        x = velocity.variables['x'][:]
        y = np.flipud(velocity.variables['y'][:])
        nx, ny = len(x), len(y)
        dx = x[1] - x[0]

        for field_name in ['VX', 'VY', 'ERRX', 'ERRY', 'STDX', 'STDY', 'CNT']:
            field = GridData((x[0], y[0]), dx, np.flipud(velocity[field_name]))

            for region in regions['features']:
                region_name = region['properties']['name'].lower()
                filename = region_name + "-" + field_name.lower() + ".txt"

                if not os.path.exists(filename):
                    with open(filename, 'w') as output_file:
                        box = region['geometry']['coordinates']
                        arcinfo.write(output_file, field.subset(*box), -2e9)

if __name__ == "__main__":
    main()
