.DEFAULT_GOAL := help

## GENERAL ##
OWNER               = backend-corps
SERVICE_NAME        = shazam
USERNAME_LOCAL      ?= "$(shell whoami)"
UID_LOCAL           ?= "$(shell id -u)"
GID_LOCAL           ?= "$(shell id -g)"

## DEV ##
DOCKER_NETWORK      = services_network
TAG_CLI             = cli
TAG_DEV             = dev

## DEPLOY ##
ENV                 ?= dev
CYBORG_BUCKET       ?= project-cyborg.${ENV}
DEPLOY_REGION       ?= sa-east-1

## RESULT VARS ##
PROJECT_NAME        = ${OWNER}-${ENV}-${SERVICE_NAME}
CONTAINER_NAME      = ${PROJECT_NAME}_backend
IMAGE_CLI           = ${PROJECT_NAME}:${TAG_CLI}
IMAGE_DEV           = ${PROJECT_NAME}:${TAG_DEV}

## CUSTOM ##
COMMAND             ?= pip install -r ./requirements.txt
PROJECT_DOMAIN      = shazam.test


build: ## make build
	@tee docker/latest/resources/requirements.txt docker/cli/resources/requirements.txt < src/requirements.txt

	docker build -f docker/cli/Dockerfile \
						--build-arg USERNAME_LOCAL=$(USERNAME_LOCAL) \
						--build-arg UID_LOCAL=$(UID_LOCAL) \
						--build-arg GID_LOCAL=$(GID_LOCAL) \
						-t ${IMAGE_CLI} docker/cli

	docker build -f docker/latest/Dockerfile \
						--build-arg IMAGE_CLI=${IMAGE_CLI} \
						-t ${IMAGE_DEV} docker/latest

	@rm -f docker/latest/resources/requirements.txt docker/cli/resources/requirements.txt

up: ## start up the container
	@make verify_network &> /dev/null
	@IMAGE_DEV=${IMAGE_DEV} \
	CONTAINER_NAME=${CONTAINER_NAME} \
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	docker-compose -p ${SERVICE_NAME} up -d backend
	@make status
	@make add_local_domain HOST_NAME=${PROJECT_DOMAIN}

stop: ## stop the container
	@make verify_network &> /dev/null
	@IMAGE_DEV=${IMAGE_DEV} \
	CONTAINER_NAME=${CONTAINER_NAME} \
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	docker-compose -p ${SERVICE_NAME} stop
	@make status

command: ## run command
	@ENV_FILE=$$(mktemp /tmp/shazam_db_env.XXXXXX); \
	chmod 0600 "$$ENV_FILE"; \
	trap 'rm -f "$$ENV_FILE"' EXIT INT TERM; \
	python3 -c "import json, os; p = 'src/.chalice/config.json'; cfg = json.load(open(p)) if os.path.exists(p) else {}; ev = cfg.get('stages', {}).get(os.environ.get('ENV', 'dev'), {}).get('environment_variables', {}); [print(f'{k}={v}') for k, v in ev.items() if k.startswith('DB_')]" > "$$ENV_FILE"; \
	ENV_ARG=""; \
	if [ -s "$$ENV_FILE" ]; then \
		ENV_ARG="--env-file $$ENV_FILE"; \
	fi; \
	docker run --rm -u ${UID_LOCAL}:${GID_LOCAL} -t \
				--net $(DOCKER_NETWORK) \
				-v $$PWD/src:/app \
				-v $$PWD/docs:/docs \
				-v $$HOME/.ssh:/home/${USERNAME_LOCAL}/.ssh \
				-v $$HOME/.aws:/home/${USERNAME_LOCAL}/.aws \
				-e AWS_DEFAULT_REGION=${DEPLOY_REGION} \
				$$ENV_ARG \
				${IMAGE_CLI} ${COMMAND}; \
	STATUS=$$?; \
	rm -f "$$ENV_FILE"; \
	exit $$STATUS


ssh: ## bash
	DOCKER_NETWORK=${DOCKER_NETWORK} \
    	docker exec -it ${CONTAINER_NAME} bash

logs:
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	docker-compose -p ${SERVICE_NAME} logs -f

status:
	DOCKER_NETWORK=${DOCKER_NETWORK} \
	PROJECT_DOMAIN=${PROJECT_DOMAIN} \
	docker-compose -p ${SERVICE_NAME} ps

# ## Deploy ##
sync-config:
	aws s3 sync s3://${CYBORG_BUCKET}/config/lambda/${OWNER}/${ENV}/${SERVICE_NAME}/ src/.chalice/

push-config:
	aws s3 sync src/.chalice s3://${CYBORG_BUCKET}/config/lambda/${OWNER}/${ENV}/${SERVICE_NAME}/ --exclude="*" --include="config.json"

install:
	@make build

deploy:
	@make sync-config install publish

add_local_domain:
	@if [ -z "${HOST_NAME}" ]; then (echo "Please set the ip in to 'HOST_NAME' variable. e.g. HOST_NAME=local.sample.test" && exit 1); fi
	$(eval ETC_HOSTS := /etc/hosts)
	$(eval IP := 127.0.0.1)
	$(eval HOSTS_LINE := '$(IP)\t$(HOST_NAME)')
	@if [ -n "$$(grep $(HOST_NAME) /etc/hosts)" ]; \
		then \
			echo "$(HOST_NAME) already exists : $$(grep $(HOST_NAME) $(ETC_HOSTS))"; \
		else \
			echo "Adding $(HOST_NAME) to your $(ETC_HOSTS)"; \
			sudo -- sh -c -e "echo $(HOSTS_LINE) >> /etc/hosts"; \
			if [ -n "$$(grep $(HOST_NAME) /etc/hosts)" ];\
				then \
					echo "$(HOST_NAME) was added succesfully \n $$(grep $(HOST_NAME) /etc/hosts)"; \
				else \
					echo "Failed to Add $(HOST_NAME), Try again!"; \
			fi \
	fi

alembic: ## run alembic command inside container, e.g. make alembic COMMAND="heads"
	@make command COMMAND="alembic $(COMMAND)"

alembic-heads: ## show alembic heads
	@make command COMMAND="alembic heads"

alembic-stamp: ## stamp database with baseline revision
	@make command COMMAND="alembic stamp 0001_baseline"

verify_network:
	@if [ -z $$(docker network ls | grep ${DOCKER_NETWORK} | awk '{print $$2}') ]; then\
	    (docker network create ${DOCKER_NETWORK});\
	fi

cli:
	PYTHONPATH=src python main.py --site ${SITE}