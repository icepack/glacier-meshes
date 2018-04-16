
.PHONY: clean

DEMS=jakobshavn-bed.txt jakobshavn-surface.txt kangerdlugssuaq-bed.txt kangerdlugssuaq-surface.txt helheim-bed.txt helheim-surface.txt

all: $(DEMS)

URL=https://daacdata.apps.nsidc.org/pub/DATASETS/IDBMG4_BedMachineGr
DEM=BedMachineGreenland-2017-09-20.nc

$(DEM):
	../scripts/fetch_nasa.sh $(URL)/$(DEM) $(DEM)

$(DEMS):
	python3 partition.py

clean:
	rm -rf $(DEM)
	rm -rf .urs_cookies
