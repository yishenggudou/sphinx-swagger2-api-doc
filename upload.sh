#!/usr/bin/env bash
which python
rm -rf build
rm -rf dist
rm -rf *.egg-info
python setup.py sdist
python setup.py install
twine upload dist/*
