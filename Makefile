MODULE=sitegen

clean:
	sudo rm -rf build dist $(MODULE).egg-info .sass-cache
	find . -name "*.pyc" -delete

install: remove _install clean

remove:
	sudo pip uninstall $(MODULE)

_install:
	sudo pip install -U .
