
import sys
from glob import glob
import geojson

def _prettify(filename, output_filename):
    with open(filename, 'r') as input_file:
        d = geojson.loads(input_file.read())

    with open(output_filename, 'w') as output_file:
        output_file.write(geojson.dumps(d, indent=2, sort_keys=True))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        for filename in glob(arg):
            _prettify(filename, filename)

