# glacier-meshes

This repository contains:
* geojson files of the outlines of several glaciers
* scripts for making a consistent orientation of the segments

The glacier outlines can be directly transformed into a mesh outline which can then be fed into a mesh generator.
In our case we use [gmsh](https://gmsh.info).
The meshes are then used in the tutorials for the glacier flow modeling library [icepack](https://www.github.com/icepack/icepack).

### Workflow

First, you'll want to create a set of shapefiles describing the boundary of a glacier catchment or a part of it.
I usually draw these by hand in QGIS.
You could also use another GIS such as Arc.
Automating this process has never worked well for me.
I try to make sure that the side wall boundaries follow glacier flowlines as closely as possible, so that there is negligible mass flux through the sides.

Next, all of the geometries need to be combined into a single GeoJSON FeatureCollection.
If you have several GeoJSON files, they can be combined into a single FeatureCollection by running the GDAL command

    ogrmerge.py <input files> \
        -single -overwrite_ds -f geojson \
        -nln <glacier name> -o <glacier name>-combined.geojson

The combined GeoJSON file can then be fixed up using the script `geomesh.py`:

    geomesh.py <glacier name>-combined.geojson --output <glacier name>.geojson

This script performs several transformations that make it easier to generate a mesh from the resulting geometry:

* Move the endpoints of each geometry so that neighboring segments' endpoints coincide exactly.
* Flip the order of some segments so that every pair of adjacent segments is oriented head-to-tail.
* Flip the order of groups of segments so that the winding number of the segments with respect to the interior of the domain is 1 and 0 w.r.t. the exterior.
* Group all segments in the same loop into the same MultiLineString.
* Make the outermost loop, which describes the boundary of the domain rather than any holes, the first item in the resulting FeatureCollection.
