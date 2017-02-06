default: c

all: c go

c: client-c server-c

go: client-go server-go

client-c: client-c.c
	gcc client-c.c -o client-c

server-c: server-c.c
	gcc server-c.c -o server-c

client-go: client-go.go
	go build client-go.go

server-go: server-go.go
	go build server-go.go

clean:
	rm -f server-c client-c server-go client-go
