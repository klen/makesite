clean:
	sudo rm -rf build dist sitegen.egg-info/
	find . -name "*.pyc" -delete

install: remove _install clean

remove:
	sudo pip uninstall sitegen

_install:
	sudo pip install -U .
