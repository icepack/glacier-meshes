
.PHONY: clean

IMAGES=jakobshavn.tif kangerdlugssuaq.tif helheim.tif

all: $(IMAGES)

URL=https://n5eil01u.ecs.nsidc.org/MEASURES/NSIDC-0547.002/2015.03.12
BIG_IMAGE=mog100_2015_hp1_v02.tif

$(BIG_IMAGE):
	../../scripts/fetch_nasa.sh $(URL)/$(BIG_IMAGE) $(BIG_IMAGE)

$(IMAGES): $(BIG_IMAGE)
	python3 ../partition.py ../../regions/greenland.geojson $(BIG_IMAGE)

clean:
	rm -f $(BIG_IMAGE)
	rm -f .urs_cookies
