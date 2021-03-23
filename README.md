# glacier-meshes

This repository contains:
* geojson files of the outlines of several glaciers
* scripts for making a consistent orientation of the segments

The glacier outlines can be directly transformed into a mesh outline which can then be fed into a mesh generator; for example we use [gmsh](https://gmsh.info) among others.
The meshes are then used in the tutorials for the glacier flow modeling library [icepack](https://www.github.com/icepack/icepack).

### Workflow

Say you want to create a glacier outline in a format that icepack can generate a mesh of.
First, you'll want to create a set of shapefiles describing the boundary of a glacier catchment or a part of it.
I usually draw these by hand in QGIS but you could use another GIS such as Arc.
Automating this process has never worked well for me.
I try to make sure that the side wall boundaries follow glacier flowlines as closely as possible, so that there is negligible mass flux through the sides.
Alternatively, you could find an outline from the [Randolph Glacier Inventory](https://www.glims.org/RGI/).
But the RGI polygons often have so much detail that the resulting mesh is too fine to run reasonable simulations, so it may be worth your while to simplify the shape.
Additionally, the RGI polygons don't distinguish between the inflow, outflow, and side wall boundaries of glaciers.

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

All of the GeoJSON files that live under the directory `glaciers/` have already been through this process, so they're in the *schema* that the icepack meshing tools expect.

### Contributing outlines

We (the developers of icepack) use the outlines in this repository for the tutorials that use real data, and so we've included outlines for the glaciers that we happen to work on.
But you (J Average Glaciologist) are welcome to contribute outlines as well.
You can submit a new outline by making a pull request on GitHub.
You'll also have to add that outline to the registry within icepack, which lives in the file `icepack/registry-outlines.txt`.
You can regenerate this registry file from the outlines here and any new outlines you've added with the following shell command:

    ls ./glaciers/ | xargs sha256sum | awk ' { t = $1; $1 = $2; $2 = t; print; } ' > registry-outlines.txt

This command will generate a text file with the list of all the outline names and their SHA256 checksums, which we need to be able to fetch them properly.
