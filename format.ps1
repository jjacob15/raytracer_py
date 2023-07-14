echo "running autopep8"
autopep8 --in-place --aggressive --in-place --recursive .\raytracer\
autopep8 --in-place --aggressive --in-place --recursive .\tests\
autopep8 --in-place --aggressive --in-place --recursive .\raytracer_demo\

echo "running flake8"
flake8 .\raytracer\
flake8 .\tests\
flake8 .\raytracer_demo\