default: all

all: http_proxy http_proxy_DNS

http_proxy: http_proxy.go
	go build http_proxy.go

http_proxy_DNS: http_proxy_DNS.go
	go build http_proxy_DNS.go

clean:
	rm -f http_proxy http_proxy_DNS
