SETTINGS=dev
PROJECT_DIR=$(CURDIR)/..
STATIC_DIR=$(PROJECT_DIR)/static
SOURCE_DIR=$(PROJECT_DIR)/source
SERVICE_DIR=$(PROJECT_DIR)/service
VIRTUALENV_DIR=$(PROJECT_DIR)/.virtualenv

.PHONY: help
# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

.PHONY: run
# target: run - Run local django dev server
run: $(VIRTUALENV_DIR)
	$(CURDIR)/manage.py runserver --settings=settings.$(SETTINGS)

.PHONY: shell
# target: shell - Run django project shell
shell: $(VIRTUALENV_DIR)
	./manage.py shell --settings=settings.$(SETTINGS)

.PHONY: test
# target: test - Run django project tests
test: $(VIRTUALENV_DIR)
	./manage.py test main --settings=settings.test

.PHONY: audit
# target: audit - Audit project code
audit:
	pylama $(SOURCE_DIR) -i E501

.PHONY: clean
# target: clean - Clean project files
clean:
	find . -name "*.pyc" -delete
	find . -name "*.orig" -delete
	find $(STATIC_DIR) -name "*.js" -delete
	find $(STATIC_DIR) -name "*.css" -delete

.PHONY: chown
# target: chown - Set current user as project files owner
chown:
	sudo chown -R $(USER):$(USER) $(SOURCE_DIR)
	sudo chown -R $(USER):$(USER) $(STATIC_DIR)
	sudo chown -R $(USER):$(USER) $(VIRTUALENV_DIR)

.PHONY: update
# target: update - Compile static and restart service
update: $(VIRTUALENV_DIR) $(SOURCE_DIR) restart chown

.PHONY: static
# target: static - Compile static
static: $(SOURCE_DIR)

.PHONY: restart
# target: restart - Restart service
restart:
	$(SERVICE_DIR)/supervisor_update.sh

$(VIRTUALENV_DIR): requirements.txt
	$(SERVICE_DIR)/virtualenv_update.sh

$(SOURCE_DIR): chown
	./manage.py collectstatic --noinput --settings=settings.$(SETTINGS)
	zeta $(STATIC_DIR)
