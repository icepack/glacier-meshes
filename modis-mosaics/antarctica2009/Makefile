
.PHONY: clean

IMAGES=amery.tif amundsen.tif filchner-ronne.tif larsen.tif ross.tif

all: $(IMAGES)

URL=https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0593_moa2009/geotiff/
BIG_IMAGE=moa125_2009_hp1_v01.1.tif

$(BIG_IMAGE).gz:
	../../scripts/fetch_nasa.sh $(URL)/$@

$(BIG_IMAGE): $(BIG_IMAGE).gz
	gunzip $(BIG_IMAGE).gz

$(IMAGES): $(BIG_IMAGE)
	python3 ../partition.py ../../regions/antarctica.geojson $(BIG_IMAGE)

clean:
	rm -rf $(BIG_IMAGE) $(BIG_IMAGE).gz
