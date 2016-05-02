CGO_ENABLED=0
GOOS=linux
GOARCH=amd64
TAG=${TAG:-latest}
COMMIT=`git rev-parse --short HEAD`

all: clean image

clean:
	@rm -rf tim2/uks-project

image:
	@echo Building Shipyard image $(TAG)
	@docker build -t tim2/uks-project .

release: build image
	@docker push tim2/uks-project

.PHONY: all build clean image release
