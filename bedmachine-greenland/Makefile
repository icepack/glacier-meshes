
.PHONY: clean

DEMS=jakobshavn-bed.tif jakobshavn-surface.tif kangerdlugssuaq-bed.tif kangerdlugssuaq-surface.tif helheim-bed.tif helheim-surface.tif

all: $(DEMS)

URL=https://daacdata.apps.nsidc.org/pub/DATASETS/IDBMG4_BedMachineGr
DEM=BedMachineGreenland-2017-09-20.nc

$(DEM):
	../scripts/fetch_nasa.sh $(URL)/$(DEM) $(DEM)

$(DEMS): $(DEM)
	python3 partition.py

clean:
	rm -rf $(DEM)
	rm -rf .urs_cookies
