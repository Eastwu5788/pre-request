#!/usr/bin/env bash

rm -vrf ./build ./dist  ./*.pyc ./*.tgz ./*.egg-info

./venv/bin/python setup.py sdist
./venv/bin/pip wheel --wheel-dir=./dist ./

./venv/bin/twine upload dist/*
