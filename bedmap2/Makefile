
.PHONY: all clean

REGIONS=amery amundsen filchner-ronne larsen ross
all: $(REGIONS:=-h.tif)

$(REGIONS:=-h.tif): bedmap2_tiff
	python3 partition.py

bedmap2_tiff: bedmap2_tiff.zip
	unzip bedmap2_tiff.zip

bedmap2_tiff.zip:
	curl -O https://secure.antarctica.ac.uk/data/bedmap2/bedmap2_tiff.zip

clean:
	rm bedmap2_tiff.zip
	rm -rf bedmap2_tiff

