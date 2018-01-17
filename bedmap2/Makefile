
.PHONY: clean

bedmap2_ascii.zip:
	curl -O https://secure.antarctica.ac.uk/data/bedmap2/bedmap2_ascii.zip

bedmap2_ascii: bedmap2_ascii.zip
	unzip bedmap2_ascii.zip

all: bedmap2_ascii

clean:
	rm bedmap2_ascii.zip
	rm -rf bedmap2_ascii

