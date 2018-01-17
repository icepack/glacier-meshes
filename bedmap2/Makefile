
.PHONY: clean

DEMS=amery-h.txt amundsen-h.txt filchner-ronne-h.txt larsen-h.txt ross-h.txt

all: $(DEMS)

%-h.txt: bedmap2_ascii
	python3 partition.py

bedmap2_ascii: bedmap2_ascii.zip
	unzip bedmap2_ascii.zip

bedmap2_ascii.zip:
	curl -O https://secure.antarctica.ac.uk/data/bedmap2/bedmap2_ascii.zip

clean:
	rm bedmap2_ascii.zip
	rm -rf bedmap2_ascii

