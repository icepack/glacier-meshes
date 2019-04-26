import geojson
from icepack.grid import geotiff

def main():
    # Read in the thickness map
    h = geotiff.read('bedmap2_tiff/bedmap2_thickness.tif')
    mask = geotiff.read('bedmap2_tiff/bedmap2_icemask_grounded_and_shelves.tif')

    # Get a list of interesting regions in Antarctica
    with open('../regions/antarctica.geojson', 'r') as regions_file:
        regions = geojson.loads(regions_file.read())

    # Save a section of the thickness map for each region to a separate file
    for region in regions['features']:
        region_name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        geotiff.write(region_name + '-h.tif', h.subset(box[0], box[1]),
                      missing=-9999, crs='epsg:3031')
        geotiff.write(region_name + '-mask.tif', mask.subset(box[0], box[1]),
                      missing=-9999, crs='epsg:3031')

if __name__ == "__main__":
    main()
