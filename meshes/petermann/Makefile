
.PHONY: clean

INPUTS=petermann-front.geojson petermann-inflow.geojson petermann-west-side.geojson petermann-east-side.geojson

petermann.msh: petermann.geo
	gmsh -2 -format msh2 petermann.geo

petermann.geo: $(INPUTS)
	python3 ../../scripts/geojson_to_mesh.py --tolerance 4e3 --output $@ --input $^

clean:
	rm -rf petermann.geo petermann.msh
