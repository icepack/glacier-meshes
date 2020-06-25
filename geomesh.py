# Copyright (C) 2019-2020 by Daniel Shapero <shapero@uw.edu>
#
# This file is part of icepack.
#
# icepack is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# The full text of the license can be found in the file LICENSE in the
# icepack source directory or at <http://www.gnu.org/licenses/>.

import argparse
import geojson
from icepack.meshing import normalize

description = """Normalize GeoJSON into a form that can be meshed easily

This script is used to turn an unordered and unoriented set of GeoJSON data
into a single GeoJSON FeatureCollection that can easily be transformed into
a planar straight-line graph for use in a computational mesh generator such
as gmsh or Triangle."""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('input', help='Path to input file')
    parser.add_argument('-o', '--output', dest='output',
                        default='output.geojson',
                        help='Path to output file')

    args = parser.parse_args()

    with open(args.input, 'r') as input_file:
        input_collection = geojson.load(input_file)

    output_collection = normalize(input_collection)
    with open(args.output, 'w') as output_file:
        geojson.dump(output_collection, output_file, indent=2)
