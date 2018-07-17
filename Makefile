NAME := boxgen

all: build

release: build
	twine upload dist/*

build:
	pip3 install wheel twine
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build release dist ${NAME}.egg-info

.PHONY: release build clean
