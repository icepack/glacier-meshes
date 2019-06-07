import copy
import glob
import itertools
import argparse
import numpy as np
import shapely.geometry
import geojson


def flatten(features):
    r"""Expand all MultiLineString features in the input list to individual
    LineString features
    """
    flat_features = []
    for feature in features:
        if feature['geometry']['type'] == 'LineString':
            flat_features.append(feature)
        if feature['geometry']['type'] == 'MultiLineString':
            properties = feature['properties']
            for line_string in feature['geometry']['coordinates']:
                geometry = geojson.LineString(coordinates=line_string)
                flat_feature = geojson.Feature(geometry=geometry,
                                               properties=properties)
                flat_features.append(flat_feature)

    return flat_features


def dist(x, y):
    return np.sqrt(sum((x - y)**2))


def closest_endpoint(features, feature_index, point_index):
    r"""Return the feature and endpoint in a collection that is closest to the
    given feature and endpoint

    The result could be the opposite endpoint of the same feature."""
    feature = features[feature_index]
    x = np.array(feature['geometry']['coordinates'][point_index])

    min_distance = np.inf
    min_findex = None
    min_pindex = None

    for findex in set(range(len(features))) - set([feature_index]):
        for pindex in (0, -1):
            y = features[findex]['geometry']['coordinates'][pindex]
            distance = dist(x, y)
            if distance < min_distance:
                min_distance = distance
                min_findex = findex
                min_pindex = pindex

    pindex = 0 if point_index == -1 else -1
    y = features[feature_index]['geometry']['coordinates'][pindex]
    if dist(x, y) < min_distance:
        min_findex = feature_index
        min_pindex = pindex

    return min_findex, min_pindex


def compute_feature_adjacency(features):
    r"""Return an integer matrix representing the adjacency between features

    An entry `A[i, j] = +1` means that the tail of feature `i` is connected to
    feature `j`, while an entry `A[i, j] = -1` means that the head of feature
    `i` is connected to feature `j`. To read off how feature `j` in turn
    connects back to feature `i`, i.e. through the head or tail, one has to
    look at the entry `A[j, i]`.
    """
    n = len(features)
    adjacency = np.zeros((n, n), dtype=int)

    for i in range(n):
        j = closest_endpoint(features, i, -1)[0]
        adjacency[i, j] += 1

        j = closest_endpoint(features, i, 0)[0]
        adjacency[i, j] -= 1

    return adjacency


def snap(input_features):
    r"""Reposition the endpoints of all features so that they are identical to
    the endpoint of the feature they are adjacent to
    """
    features = copy.deepcopy(input_features)
    adjacency = compute_feature_adjacency(features)

    for i, j in zip(*np.nonzero(adjacency)):
        ei = -1 if adjacency[i, j] == 1 else 0
        ej = -1 if adjacency[j, i] == 1 else 0

        xi = features[i]['geometry']['coordinates'][ei]
        xj = features[j]['geometry']['coordinates'][ej]
        average = ((np.array(xi) + np.array(xj)) / 2).tolist()

        features[i]['geometry']['coordinates'][ei] = average
        features[j]['geometry']['coordinates'][ej] = average

    for i in np.flatnonzero(np.count_nonzero(adjacency, 1) == 0):
        xi = features[i]['geometry']['coordinates'][0]
        xj = features[i]['geometry']['coordinates'][-1]
        average = ((np.array(xi) + np.array(xj)) / 2).tolist()

        features[i]['geometry']['coordinates'][0] = average
        features[i]['geometry']['coordinates'][-1] = average

    return features


def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r)
                                         for r in range(len(s) + 1))


def reorient(input_features):
    r"""Flip the order of all features so that they are always oriented head-
    to-tail
    """
    features = copy.deepcopy(input_features)
    adjacency = compute_feature_adjacency(features)

    if np.count_nonzero(adjacency + adjacency.T) == 0:
        return features

    sets = powerset(range(len(features)))
    for s in sets:
        A = np.copy(adjacency)
        for i in s:
            A[i, :] *= -1

        if np.count_nonzero(A + A.T) == 0:
            for i in s:
                coords = features[i]['geometry']['coordinates']
                features[i]['geometry']['coordinates'] = coords[::-1]

            return features

    raise ValueError('This cannot be.')


def features_to_loops(features):
    r"""Return a list of lists of the segments in each loop, in order
    """
    adjacency = compute_feature_adjacency(features)

    # Add all the single-feature loops
    feature_indices = set(range(len(features)))
    loops = []
    for index in range(len(features)):
        if np.count_nonzero(adjacency[index, :]) == 0:
            loops.append([index])
            feature_indices.remove(index)

    # Add all the multi-feature loops
    while feature_indices:
        start_index = feature_indices.pop()
        loop = [start_index]
        index = np.flatnonzero(adjacency[start_index, :] == 1)[0]
        while index != start_index:
            feature_indices.remove(index)
            loop.append(index)
            index = np.flatnonzero(adjacency[index, :] == 1)[0]

        loops.append(loop)

    return loops


def topologize(input_features):
    r"""Return a FeatureCollection of MultiLineStrings, one for each loop
    """
    loops = features_to_loops(input_features)
    features = []
    for loop in loops:
        coords = [list(geojson.utils.coords(input_features[index]))
                  for index in loop]
        multi_line_string = geojson.MultiLineString(coords)
        features.append(geojson.Feature(geometry=multi_line_string))

    return features


def find_bounding_feature(features):
    r"""Return the index of the feature in the collection that contains all
    other features
    """
    line_strings = [sum(feature['geometry']['coordinates'], [])
                    for feature in features]
    polygons = [shapely.geometry.Polygon(line_string)
                for line_string in line_strings]

    for index, poly in enumerate(polygons):
        if all([poly.contains(p) for p in polygons if p is not poly]):
            return index

    raise ValueError('No polygon contains all other polygons!')


def reorder(input_features):
    features = copy.deepcopy(input_features)
    index = find_bounding_feature(features)
    bounding_feature = features.pop(index)
    return [bounding_feature] + features


def main(collection):
    features = collection['features']
    collection['features'] = \
        reorder(topologize(reorient(snap(flatten(features)))))
    return collection

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

    output_collection = main(input_collection)
    with open(args.output, 'w') as output_file:
        geojson.dump(output_collection, output_file, indent=2)
