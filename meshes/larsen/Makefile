
.PHONY: clean

INPUTS=larsen_front0.geojson larsen_front1.geojson larsen_gipps_ice_rise.geojson larsen_inflow.geojson larsen_island0.geojson larsen_island1.geojson larsen_side0.geojson larsen_side1.geojson

larsen.msh: larsen.geo
	gmsh -2 -format msh2 larsen.geo

larsen.geo: $(INPUTS)
	python3 ../../scripts/geojson_to_mesh.py --tolerance 10e3 --output $@ --input $^

clean:
	rm -rf larsen.geo larsen.msh
