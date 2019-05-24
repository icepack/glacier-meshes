import geojson
import rasterio

def main():
    # Read in the thickness map
    h = rasterio.open('bedmap2_tiff/bedmap2_thickness.tif', 'r')
    opts = {'transform': h.transform, 'height': h.height, 'width': h.width}

    # Get a list of interesting regions in Antarctica
    with open('../regions/antarctica.geojson', 'r') as regions_file:
        regions = geojson.loads(regions_file.read())

    # Save a section of the thickness map for each region to a separate file
    for region in regions['features']:
        name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        window = rasterio.windows.from_bounds(*box[0], *box[1], **opts)
        profile = h.profile.copy()
        profile['height'] = window.height
        profile['width'] = window.width
        profile['transform'] = rasterio.windows.transform(window, h.transform)

        with rasterio.open(name + '-h.tif', 'w', **profile) as destination:
            data = h.read(indexes=1, masked=True, window=window)
            destination.write(data, indexes=1)

if __name__ == "__main__":
    main()
