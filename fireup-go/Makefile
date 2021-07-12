BIN_PATH=$(GOPATH)/bin/fireup

all: build 
build:
	go build -o fireup -v
buildbin: 
	go build -o $(BIN_PATH)
run: 
	@go run main.go -o go.mod -d apk/a.md