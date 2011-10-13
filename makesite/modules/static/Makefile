DEPLOY_DIR=../
SERVICE_DIR=../service

update: static chown

static:
	$(SERVICE_DIR)/html_install_update.sh

chown:
	sudo chown -R $(USER):$(USER) $(DEPLOY_DIR)
