import argparse
from itertools import chain, combinations
import numpy as np
import geojson

def dist(x, y):
    return np.sqrt(sum((x - y)**2))


def _extract_feature(feature):
    if feature['geometry']['type'] == 'MultiLineString':
        return [np.array(line) for line in feature['geometry']['coordinates']]
    elif feature['geometry']['type'] == 'LineString':
        return [np.array(feature['geometry']['coordinates'])]
    raise ValueError()


def _read_geojson(geojson_file):
    dataset = geojson.loads(geojson_file.read())

    lines = []
    for feature in dataset['features']:
        lines.extend(_extract_feature(feature))

    return lines


def _find_adjacent_segment(segments, i, tolerance, endpoint='tail'):
    """Return the segment adjacent to the tail of a given segment."""
    X = segments[i]
    if dist(X[0], X[-1]) < tolerance:
        return i

    index = -1 if endpoint == 'tail' else 0
    from itertools import chain
    for j in chain(range(i), range(i + 1, len(segments))):
        Y = segments[j]

        if ((dist(X[index], Y[0]) < tolerance) or
            (dist(X[index], Y[-1]) < tolerance)):
            return j

    raise ValueError("No segment is adjacent to {0}!".format(i))


def _compute_segment_adjacency(segments, tolerance):
    n = len(segments)
    A = np.zeros((n, n), dtype=int)

    for i in range(n):
        j = _find_adjacent_segment(segments, i, tolerance, 'tail')
        A[i, j] += 1

        j = _find_adjacent_segment(segments, i, tolerance, 'head')
        A[i, j] -= 1

    return A


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def _orient_segments(segments, tolerance):
    """Reverse some segments as need be for orientability."""
    A = _compute_segment_adjacency(segments, tolerance)

    if np.count_nonzero(A + A.T) == 0:
        return

    sets = powerset(list(range(len(segments))))
    for s in sets:
        B = np.copy(A)
        for i in s:
            B[i,:] *= -1

        if np.count_nonzero(B + B.T) == 0:
            for i in s:
                segments[i] = segments[i][::-1,:]

            A = _compute_segment_adjacency(segments, tolerance)
            if np.count_nonzero(A + A.T) > 0:
                raise ValueError("This cannot be.")

            return


def _segments_to_loops(segments, adjacency):
    """Return a list of lists describing each loop of the PSLG"""
    A = np.copy(adjacency)

    n = len(segments)
    loops = []
    for i in range(n):
        if np.count_nonzero(A[i, :]) == 0:
            loops.append([i])

    while np.count_nonzero(A) > 0:
        nz = A.nonzero()
        i = nz[0][0]
        j = np.argmax(A[i, :])
        A[i, :] = 0

        loop = [i]
        while j != i:
            loop.append(j)
            row = A[j, :].copy()
            A[j, :] = 0
            j = np.argmax(row)

        loops.append(loop)

    return loops


def _next_segment_in_loop(loops, n):
    for loop in loops:
        if n in loop:
            return loop[(loop.index(n) + 1) % len(loop)]

    raise ValueError("Gross.")


def _segments_to_pslg(_segments, tolerance):
    """Convert the segments to a planar straight-line graph"""
    segments = [segment.copy() for segment in _segments]

    _orient_segments(segments, tolerance)
    adjacency = _compute_segment_adjacency(segments, tolerance)
    loops = _segments_to_loops(segments, adjacency)

    segments = [segment[:-1, :] for segment in segments]
    points = np.concatenate(segments)

    cumulative_point_count = [0]
    for segment in segments:
        count = cumulative_point_count[-1]
        cumulative_point_count.append(count + len(segment))

    num_points = cumulative_point_count[-1]
    edges = np.zeros((num_points, 2), dtype=int)
    edge_ids = np.zeros(num_points, dtype=int)

    for n in range(len(segments)):
        p = cumulative_point_count[n]
        for k in range(len(segments[n]) - 1):
            edges[p + k, :] = (p + k, p + k + 1)

        k = len(segments[n]) - 1
        m = _next_segment_in_loop(loops, n)
        edges[p + k, :] = (p + k, cumulative_point_count[m])

        edge_ids[p: p + len(segments[n])] = n

    return points, edges, edge_ids, loops


def _pslg_to_geo(geo_file, points, edges, edge_ids, loops, resolution=1e12):
    geo_file.write("cl = {};\n\n".format(resolution))

    # Write out all the points, lines, line loops, and surfaces
    num_points = len(points)
    for n in range(num_points):
        x = points[n, :]
        geo_file.write("Point({0}) = {{{1}, {2}, 0.0, cl}};\n"
                       .format(n + 1, x[0], x[1]))
    geo_file.write("\n")

    num_edges = len(edges)
    for n in range(num_edges):
        i, j = edges[n, :]
        geo_file.write("Line({0}) = {{{1}, {2}}};\n"
                       .format(n + 1, i + 1, j + 1))
    geo_file.write("\n")

    def stringify(items):
        return [str(i) for i in items]

    num_edge_ids = len(set(edge_ids))
    for l in range(len(loops)):
        loop = loops[l]
        geo_file.write("Line Loop({0}) = {{".format(l + 1))
        loop_edges = [i + 1 for i in range(num_edges) for edge_id in loop
                      if edge_ids[i] == edge_id]
        geo_file.write(", ".join(stringify(loop_edges)))
        geo_file.write("};\n")
    geo_file.write("\n")

    geo_file.write("Plane Surface(1) = {{{0}}};\n\n"
                   .format(', '.join(stringify(range(1, len(loops) + 1)))))

    # Write out all the physical lines and surfaces
    for edge_id in sorted(list(set(edge_ids))):
        indices = [i + 1 for i in range(num_edges) if edge_ids[i] == edge_id]
        geo_file.write("Physical Line({0}) = {{{1}}};\n"
                       .format(edge_id + 1, ', '.join(stringify(indices))))
    geo_file.write("\n")

    unique_ids = [k + 1 for k in sorted(list(set(edge_ids)))]
    geo_file.write("Physical Surface(1) = {{{0}}};\n"
                   .format(', '.join(stringify(unique_ids))))


def main(outfile, infiles, tolerance, resolution):
    segments = sum([_read_geojson(open(f, 'r')) for f in infiles], [])

    points, edges, edge_ids, loops = _segments_to_pslg(segments, tolerance)

    with open(outfile, 'w') as geo_file:
        _pslg_to_geo(geo_file, points, edges, edge_ids, loops, resolution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a mesh outline from several GeoJSON files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--output', required=True,
                        help="Name of output file")
    parser.add_argument('--input', required=True, nargs='*',
                        help="Names of input GeoJSON files")
    parser.add_argument('--tolerance', type=float, default=10e3,
                        help="Tolerance for snapping segments together")
    parser.add_argument('--resolution', type=float, default=1e12,
                        help="Mesh resolution")
    args = parser.parse_args()

    main(args.output, args.input, args.tolerance, args.resolution)

