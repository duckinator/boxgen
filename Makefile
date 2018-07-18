NAME := boxgen

all: build

release: build
	twine upload dist/*

build:
	python3 setup.py build

clean:
	python3 setup.py clean

.PHONY: release build clean
