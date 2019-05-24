import geojson
import rasterio

def main():
    with open("../regions/greenland.geojson", 'r') as geojson_file:
        regions = geojson.loads(geojson_file.read())

    for field_name in ['surface', 'bed']:
        ident = 'netcdf:BedMachineGreenland-2017-09-20.nc:' + field_name
        field = rasterio.open(ident, 'r')

        for region in regions['features']:
            region_name = region['properties']['name'].lower()
            output_filename = region_name + '-' + field_name + '.tif'
            box = region['geometry']['coordinates']

            window = rasterio.windows.from_bounds(
                *box[0], *box[1], field.transform, field.height, field.width)
            data = field.read(indexes=1, window=window, masked=True)
            transform = rasterio.windows.transform(window, field.transform)
            profile = field.profile.copy()
            profile.update(height=window.height, width=window.width,
                           transform=transform, driver='GTiff')
            with rasterio.open(output_filename, 'w', **profile) as destination:
                destination.write(data, indexes=1)

if __name__ == "__main__":
    main()
