SETTINGS=dev
STATIC_DIR=../static
SOURCE_DIR=../source
SERVICE_DIR=../service

run:
	./manage.py runserver --settings=settings.$(SETTINGS)

shell:
	./manage.py shell --settings=settings.$(SETTINGS)

test:
	./manage.py test main --settings=settings.test

clean:
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete
	sudo rm -rf .sass-cache

update: static ve_update restart chown

static: chown collect zeta

restart:
	sudo sh $(SERVICE_DIR)/restart_update.sh

ve_update:
	sudo sh $(SERVICE_DIR)/virtualenv_update.sh

chown:
	sudo chown -R $(USER):$(USER) $(STATIC_DIR)
	sudo chown -R $(USER):$(USER) $(SOURCE_DIR)

collect:
	./manage.py collectstatic --noinput --settings=settings.$(SETTINGS)

zeta:
	zeta $(STATIC_DIR)
