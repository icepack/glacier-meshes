
import geojson
import rasterio

def main():
    with open("../regions/antarctica.geojson", 'r') as geojson_file:
        regions = geojson.loads(geojson_file.read())

    filename = "moa125_2009_hp1_v1.1.tif"
    with rasterio.drivers():
        with rasterio.open(filename, 'r') as source:
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
    main()
