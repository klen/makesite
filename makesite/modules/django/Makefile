SETTINGS=dev
STATIC_DIR=../static
SOURCE_DIR=../source
SERVICE_DIR=../service

run:
	# Run local django dev server
	./manage.py runserver --settings=settings.$(SETTINGS)

shell:
	# Run django project shell
	./manage.py shell --settings=settings.$(SETTINGS)

test:
	# Test project
	./manage.py test main --settings=settings.test

clean:
	# Clean project
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete

clean_static:
	sudo rm -rf $(STATIC_DIR)/*.js
	sudo rm -rf $(STATIC_DIR)/*.css
	sudo rm -rf $(STATIC_DIR)/*/

update: static ve_update restart chown

static: chown collect zeta

restart:
	sudo sh $(SERVICE_DIR)/supervisor_update.sh

ve_update:
	sudo sh $(SERVICE_DIR)/virtualenv_update.sh

chown:
	sudo chown -R $(USER):$(USER) $(STATIC_DIR)
	sudo chown -R $(USER):$(USER) $(SOURCE_DIR)

collect:
	./manage.py collectstatic --noinput --settings=settings.$(SETTINGS)

zeta:
	zeta $(STATIC_DIR)
