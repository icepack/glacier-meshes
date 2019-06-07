# glacier-meshes

This repository contains:
* geojson files of the outlines of several glaciers
* scripts for making a consistent orientation of the segments

The glacier outlines can be directly transformed into a mesh outline which can then be fed into a mesh generator.
In our case we use [gmsh](https://gmsh.info).
The meshes are then used in the tutorials for the glacier flow modeling library [icepack](https://www.github.com/icepack/icepack).
