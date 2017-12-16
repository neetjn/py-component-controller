clean:
	rm -rf build dist *.egg-info venv *.pyc .cache
	rm -rf pyscc/*.pyc tests/*.pyc tests/__pycache__

setup:
# create virtualenv and install test dependencies
	virtualenv venv && venv/bin/pip install -r tests/test-requirements.txt
	git submodule init
	git submodule update
	npm --prefix tests/mock-site install

app:
	npm run --prefix tests/mock-site app:detached

test:
# run e2e tests
	venv/bin/pytest --cov=pyscc tests/test_*.py

package:
	python setup.py sdist

publish: package
	twine upload dist/*
