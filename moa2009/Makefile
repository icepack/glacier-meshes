
.PHONY: clean

IMAGES=amery.tif amundsen.tif filchner-ronne.tif larsen.tif ross.tif

all: $(IMAGES)

$(IMAGES): moa125_2009_hp1_v1.1.tif
	python3 partition.py

URL=ftp://sidads.colorado.edu/pub/DATASETS/nsidc0593_moa2009/geotiff

moa125_2009_hp1_v1.1.tif.gz:
	curl $(URL)/moa125_2009_hp1_v1.1.tif.gz -o moa125_2009_hp1_v1.1.tif.gz

moa125_2009_hp1_v1.1.tif: moa125_2009_hp1_v1.1.tif.gz
	gunzip moa125_2009_hp1_v1.1.tif.gz

clean:
	rm -rf moa125_2009_hp1_v1.1.tif.gz moa125_2009_hp1_v1.1.tif

