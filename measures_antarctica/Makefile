
.PHONY: clean

VELOCITIES= amery-vx.txt amundsen-vx.txt filchner-ronne-vx.txt larsen-vx.txt ross-vx.txt amery-vy.txt amundsen-vy.txt filchner-ronne-vy.txt larsen-vy.txt ross-vy.txt

all: $(VELOCITIES)

%.txt: antarctica_ice_velocity_900m.nc
	python3 partition.py

URL=https://n5eil01u.ecs.nsidc.org/MEASURES/NSIDC-0484.001/1996.01.01

antarctica_ice_velocity_900m.nc:
	../scripts/fetch_nasa.sh \
	  $(URL)/antarctica_ice_velocity_900m.nc antarctica_ice_velocity_900m.nc

clean:
	rm -f antarctica_ice_velocity_900m.nc
	rm -f .urs_cookies

