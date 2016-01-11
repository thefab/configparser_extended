default: all

all:
	python setup.py build

install: all
	python setup.py install

clean:
	rm -f *.pyc
	cd tests && rm -f *.pyc
	cd configparser_extended && rm -f *.pyc
	cd tests && rm -Rf htmlcov 
	rm -f .coverage tests/.coverage
	rm -Rf build
	rm -Rf dist
	rm -Rf configparser_extended.egg-info
	rm -Rf configparser_extended/__pycache__
	rm -Rf tests/__pycache__
	rm -f tests/conf.py
	rm -f tests/auth.txt

sdist: clean
	python setup.py sdist

test:
	flake8 .
	cd tests && nosetests

dev: clean
	python setup.py develop

coveralls:
	cd tests && nosetests --with-coverage --cover-package=configparser_extended && ../.coveralls.sh

upload:
	python setup.py sdist register upload

coverage:
	cd tests && coverage run `which nosetests` && coverage html --include='*/configparser_extended/configparser_extended/*' --omit='test_*'

release: test coverage clean upload clean 
