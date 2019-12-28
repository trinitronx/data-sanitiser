REPO_NAME              := ppi-sanitize
SHELL                   = /bin/bash
VERSION_FILE            = VERSION
VERSION                 =`cat $(VERSION_FILE)`
PACKAGE_FILE            = $(REPO_NAME)-$(VERSION).tar.gz

# include ./build/main.mk

.PHONY: build-requirements setup sdist install test nose2

build/.pip_install_build_reqs: build/build-requirements.txt ## no-help
	pip install -r build/build-requirements.txt
	touch build/.pip_install_build_reqs
build-requirements: build/.pip_install_build_reqs ## Install setup.py requirements from build/build-requirements.txt

setup: build-requirements ## Run python setup.py sdist
	python setup.py sdist

sdist: setup ## Alias for make setup

install: build-requirements ## Runs python setup.py install
	python setup.py install

test: ## Runs tests
	python setup.py test

nose2: ## Runs tests via nose2 CLI (requires: pip3 install nose2)
	nose2

.PHONY: clean
clean:: ## Removes all temporary files - Executes make clean
	rm -rf ./dist
	rm -rf ./.eggs
	rm -f MANIFEST README.txt README.rst
	rm -f .coverage
	find ./ -type f -iwholename '*.egg-info/*' -exec rm -rf '{}' \;
	find ./ -iname '*.pyc' -exec rm -f '{}' \;
	find ./ -type f -name '__pycache__/*' -exec rm -f '{}' \;
	find ./build -type f ! \( -name 'build-requirements.txt' -o -name main.mk \) -exec rm -f '{}' \;
