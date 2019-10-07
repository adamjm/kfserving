# Build the manager binary
ARCH
FROM golang:1.10.3 as builder

# Copy in the go src
WORKDIR /go/src/github.com/kubeflow/kfserving
COPY pkg/    pkg/
COPY cmd/    cmd/
COPY vendor/ vendor/
# Build
RUN 
        CGO_ENABLED=0 GOOS=linux GOARCH=${ARCH} go build -a -o manager ./cmd/manager

# Copy the controller-manager into a thin image
FROM ${ARCH}/ubuntu:latest
WORKDIR /
COPY --from=builder /go/src/github.com/kubeflow/kfserving/manager .
ENTRYPOINT ["/manager"]
