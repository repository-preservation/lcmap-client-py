ORG = usgseros
PROJECT = ubuntu-py-lcmap-client
VERSION = 0.5.0
IMAGE = $(ORG)/$(PROJECT):$(VERSION)
CONFIG = ~/.usgs:/root/.usgs

info:
	@echo tag: $(IMAGE)
	@echo cfg: $(CONFIG)
	docker images $(IMAGE)

build:
	@docker build -t $(IMAGE) .

run: build
	@docker run --volume $(CONFIG) -it $(IMAGE)

publish: build
	@docker push $(IMAGE)
