
.PHONY: clean

VELOCITIES=kangerdlugssuaq-vx.tif kangerdlugssuaq-vy.tif helheim-vx.tif helheim-vy.tif jakobshavn-vx.tif jakobshavn-vy.tif

all: $(VELOCITIES)
URL=https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0725_MEASURES_annual_vel_mosaics_v01/2015/
FILES=greenland_vel_mosaic200_2015_vx_v01.tif greenland_vel_mosaic200_2015_vy_v01.tif greenland_vel_mosaic200_2015_ex_v01.tif greenland_vel_mosaic200_2015_ey_v01.tif


greenland_vel_mosaic200_2015_%_v01.tif:
	../../scripts/fetch_nasa.sh $(URL)/$@

$(VELOCITIES): $(FILES)
	python3 partition.py

clean:
	rm -rf $(VELOCITIES)
	rm -rf .urs_cookies
