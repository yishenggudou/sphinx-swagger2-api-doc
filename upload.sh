#!/usr/bin/env bash
which python
rm -rvf build
rm -rvf dist
rm -rvf *.egg-info
python setup.py sdist
python setup.py install
twine upload dist/*
