
.PHONY: clean

IMAGES=amery.tif amundsen.tif filchner-ronne.tif larsen.tif ross.tif

all: $(IMAGES)

URL=ftp://sidads.colorado.edu/pub/DATASETS/nsidc0593_moa2009/geotiff
BIG_IMAGE=moa125_2009_hp1_v1.1.tif

$(BIG_IMAGE).gz:
	curl $(URL)/$(BIG_IMAGE).gz -o $(BIG_IMAGE).gz

$(BIG_IMAGE): $(BIG_IMAGE).gz
	gunzip $(BIG_IMAGE).gz

$(IMAGES): $(BIG_IMAGE)
	python3 ../partition.py ../../regions/antarctica.geojson $(BIG_IMAGE)

clean:
	rm -rf $(BIG_IMAGE) $(BIG_IMAGE).gz

