#! /bin/sh
echo "running autopep8"
autopep8 --in-place --aggressive --in-place --recursive ./raytracer/
autopep8 --in-place --aggressive --in-place --recursive ./tests/
autopep8 --in-place --aggressive --in-place --recursive ./raytracer_demo/
