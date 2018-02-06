import geojson
from icepack.grid import arcinfo

def main():
    # Read in the thickness map
    with open("bedmap2_ascii/bedmap2_thickness.txt", 'r') as thickness_file:
        h = arcinfo.read(thickness_file)

    with open("bedmap2_ascii/"
              "bedmap2_icemask_grounded_and_shelves.txt", 'r') as mask_file:
        mask = arcinfo.read(mask_file)

    # Get a list of interesting regions in Antarctica
    with open("../regions/antarctica.geojson", 'r') as regions_file:
        regions = geojson.loads(regions_file.read())

    # Save a section of the thickness map for each region to a separate file
    for region in regions['features']:
        region_name = region['properties']['name'].lower()
        box = region['geometry']['coordinates']

        with open(region_name + "-h.txt", 'w') as region_thickness:
            arcinfo.write(region_thickness, h.subset(box[0], box[1]), -9999)

        with open(region_name + "-mask.txt", 'w') as region_mask:
            arcinfo.write(region_mask, mask.subset(box[0], box[1]), -9999)

if __name__ == "__main__":
    main()
