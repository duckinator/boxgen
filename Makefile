NAME := boxgen

all: build

release: build
	twine upload dist/*

build:
	python3 setup.py build

clean:
	rm -rf build release dist ${NAME}.egg-info

.PHONY: release build clean
