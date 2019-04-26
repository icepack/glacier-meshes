
.PHONY: clean

VELOCITIES= amery-vx.tif amundsen-vx.tif filchner-ronne-vx.tif larsen-vx.tif ross-vx.tif amery-vy.tif amundsen-vy.tif filchner-ronne-vy.tif larsen-vy.tif ross-vy.tif

all: $(VELOCITIES)

%.tif: antarctica_ice_velocity_450m_v2.nc
	python3 partition.py

URL=https://n5eil01u.ecs.nsidc.org/MEASURES/NSIDC-0484.002/1996.01.01

antarctica_ice_velocity_450m_v2.nc:
	../scripts/fetch_nasa.sh \
	  $(URL)/antarctica_ice_velocity_450m_v2.nc antarctica_ice_velocity_450m_v2.nc

clean:
	rm -f antarctica_ice_velocity_450m_v2.nc
	rm -f .urs_cookies
