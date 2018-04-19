
.PHONY: clean

VELOCITIES=kangerdlugssuaq-vx.txt kangerdlugssuaq-vy.txt helheim-vx.txt helheim-vy.txt jakobshavn-vx.txt jakobshavn-vy.txt

all: $(VELOCITIES)

URL=https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0725_MEASURES_annual_vel_mosaics_v01
FILES=greenland_vel_mosaic200_2015_vx_v01.tif greenland_vel_mosaic200_2015_vy_v01.tif

greenland_vel_mosaic200_2015_%_v01.tif:
	../../scripts/fetch_nasa.sh $(URL)/$@

$(VELOCITIES): $(FILES)
	python3 partition.py

clean:
	rm -rf $(FILES)
	rm -rf .urs_cookies
