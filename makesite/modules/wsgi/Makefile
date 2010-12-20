STATIC_DIR=../static
SOURCE_DIR=../source
SERVICE_DIR=../service

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
	cp -r static/* $(STATIC_DIR)

zeta:
	zeta $(STATIC_DIR)
