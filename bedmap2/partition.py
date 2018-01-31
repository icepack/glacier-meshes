import geojson
from icepack.grid import arcinfo

def main():
    # Read in the thickness map
    with open("bedmap2_ascii/bedmap2_thickness.txt", 'r') as thickness_file:
        h = arcinfo.read(thickness_file)

    # Get a list of interesting regions in Antarctica
    with open("../regions/antarctica.geojson", 'r') as regions_file:
        regions = geojson.loads(regions_file.read())

    # Save a section of the thickness map for each region to a separate file
    for region in regions['features']:
        region_name = region['properties']['name'].lower()
        bounding_box = region['geometry']['coordinates']

        xmin, ymin = bounding_box[0]
        xmax, ymax = bounding_box[1]

        with open(region_name + "-h.txt", 'w') as region_file:
            arcinfo.write(region_file, h.subset((xmin, ymin), (xmax, ymax)), -9999)

if __name__ == "__main__":
    main()
