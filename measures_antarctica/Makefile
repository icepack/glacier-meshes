
.PHONY: clean

VELOCITIES= amery-vx.txt amundsen-vx.txt filchner-ronne-vx.txt larsen-vx.txt ross-vx.txt amery-vy.txt amundsen-vy.txt filchner-ronne-vy.txt larsen-vy.txt ross-vy.txt

all: $(VELOCITIES)

%.txt: antarctica_ice_velocity_450m_v2.nc
	python3 partition.py

URL=https://n5eil01u.ecs.nsidc.org/MEASURES/NSIDC-0484.002/1996.01.01

antarctica_ice_velocity_450m_v2.nc:
	../scripts/fetch_nasa.sh \
	  $(URL)/antarctica_ice_velocity_450m_v2.nc antarctica_ice_velocity_450m_v2.nc

clean:
	rm -f antarctica_ice_velocity_450m_v2.nc
	rm -f .urs_cookies

