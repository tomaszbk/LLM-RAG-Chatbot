# Use a specific version of golang based on Alpine for smaller image size
FROM golang:1.22-alpine as builder

# Install git, required for fetching Go dependencies.
# Many go modules are hosted on version control systems like git
RUN apk add --no-cache git

WORKDIR /app

COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go app as a static binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o kukebot-service .

# Use a minimal alpine image for the final stage
FROM alpine:latest  
WORKDIR /root/

# Copy the pre-built binary file from the previous stage
COPY --from=builder /app/kukebot-service .

CMD ["./kukebot-service"]