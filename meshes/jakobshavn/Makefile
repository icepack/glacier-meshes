
.PHONY: clean

INPUTS=jakobshavn-front.geojson jakobshavn-inflow.geojson jakobshavn-north-side.geojson jakobshavn-south-side.geojson

jakobshavn.msh: jakobshavn.geo
	gmsh -2 -format msh2 jakobshavn.geo

jakobshavn.geo: $(INPUTS)
	python3 ../../scripts/geojson_to_mesh.py --tolerance 2e3 --output $@ --input $^

clean:
	rm -rf jakobshavn.geo jakobshavn.msh
