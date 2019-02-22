
import sys
import geojson
import rasterio

def main(regions_file, big_image):
    with open(regions_file, 'r') as geojson_file:
        regions = geojson.loads(geojson_file.read())

    with rasterio.open(big_image, 'r') as source:
        for region in regions['features']:
            name = region['properties']['name'].lower()
            box = region['geometry']['coordinates']
            window = source.window(*box[0], *box[1])

            image = source.read(window=window)

            profile = source.profile
            transform = source.window_transform(window)
            profile['transform'] = transform
            profile['height'] = image.shape[1]
            profile['width'] = image.shape[2]

            with rasterio.open(name + ".tif", 'w', **profile) as dest:
                dest.write(image)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
