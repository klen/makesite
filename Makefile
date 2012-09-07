MODULE=makesite
SPHINXBUILD=sphinx-build
ALLSPHINXOPTS= -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
BUILDDIR=_build

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: clean
# target: clean - Clean module
clean:
	sudo rm -rf build dist $(MODULE).egg-info/ docs/_build
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

.PHONY: register
# target: register - Register module on PyPi
register:
	python setup.py register

.PHONY: upload
# target: upload - Upload module on PyPi
upload: docs
	python setup.py sdist upload || echo 'Upload already'

.PHONY: test
# target: test - Run module tests
test:
	python setup.py test

.PHONY: tox
# target: tox - Test module with tox
tox: .tox tox.ini
	tox

.PHONY: audit
# target: audit - Run module audit
audit:
	pylama $(MODULE) -i E501

.PHONY: docs
# target: docs - Build module docs
docs:
	python setup.py build_sphinx --source-dir=docs/ --build-dir=docs/_build --all-files
	python setup.py upload_sphinx --upload-dir=docs/_build/html

.PHONY: install
# target: install - Install current version from repo as root
install:
	sudo pip install .
