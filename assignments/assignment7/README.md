
# Assignment 7: HTTP  Proxy

### Due May 14th, 5:00pm

In this assignment, you will implement a web proxy that passes requests and data between multiple web clients and web servers. The proxy should support **concurrent** connections. This assignment will give you a chance to get to know one of the most popular application protocols on the Internet -- the Hypertext Transfer Protocol (HTTP). When you're done with the assignment, you should be able to configure Firefox to use your  proxy implementation.

You may work with a partner on this assignment.

## Introduction: The Hypertext Transfer Protocol

The Hypertext Transfer Protocol (HTTP) is the protocol used for communication on the web: it defines how your web browser requests resources from a web server and how the server responds. For simplicity, in this assignment, we will be dealing only with version 1.1 of the HTTP protocol, defined in detail in [RFC 2616](https://www.ietf.org/rfc/rfc2616.txt). You do not need to read the full text to complete this assignment. We summarize the most important parts further down.

HTTP communications happen in the form of transactions; a transaction consists of a client sending a request to a server and then reading the response. Request and response messages share a common basic format:

*   An initial line (a request or response line, as defined below)
*   Zero or more header lines
*   A blank line (CRLF)
*   An optional message body.

The initial line and header lines are each followed by a "carriage-return line-feed" (\r\n) signifying the end-of-line.

For most common HTTP transactions, the protocol boils down to a relatively simple series of steps (important sections of [RFC 2616](https://www.ietf.org/rfc/rfc2616.txt) are in parenthesis):

1.  A client creates a connection to the server.
2.  The client issues a request by sending a line of text to the server. This **request line** consists of an HTTP _method_ (most often "GET", but "POST", "PUT", and others are possible), a _request URI_ (like a URL), and the protocol version that the client wants to use ("HTTP/1.1"). The request line is followed by one or more header lines. The message body of the initial request is typically empty. (5.1-5.2, 8.1-8.3, 10, D.1)
3.  The server sends a response message, with its initial line consisting of a **status line**, indicating if the request was successful. The status line consists of the HTTP version ("HTTP/1.1"), a _response status code_ (a numerical value that indicates whether or not the request was completed successfully), and a _reason phrase_, an English-language message providing description of the status code. Just as with the request message, there can be as many or as few header fields in the response as the server wants to return. Following the CRLF field separator, the message body contains the data requested by the client in the event of a successful request. (6.1-6.2, 9.1-9.5, 10)
4.  Once the server has returned the response to the client, it closes the connection.

It's fairly easy to see this process in action without using a web browser. From your terminal, type:

`telnet www.google.com 80`

This opens a TCP connection to the server at www.google.com listening on port 80 (the default HTTP port). You should see something like this:

```
Trying 172.217.1.68...
Connected to www.google.com.
Escape character is '^]'.
```

type the following:

`GET http://www.google.com/ HTTP/1.1`

and hit enter **twice**. You should see something like the following:

```
HTTP/1.1 200 OK
Date: Fri, 17 Feb 2017 23:58:09 GMT
(More HTTP headers...)
Content-Type: text/html; charset=ISO-8859-1

<!doctype html><html itemscope="" ...
(More HTML follows)
```

There may be some additional pieces of header information as well, such as setting cookies and/or instructions to the browser or proxy on caching behavior. What you are seeing is exactly what your web browser sees when it goes to the Google home page: the HTTP status line, the header fields, and finally the HTTP message body consisting of the HTML that your browser interprets to create a web page.


### HTTP Proxies

Ordinarily, HTTP is a client-server protocol. The client (usually your web browser) communicates directly with the server (the web server software). However, in some circumstances it may be useful to introduce an intermediate entity called a proxy. Conceptually, the proxy sits between the client and the server. In the simplest case, instead of sending requests directly to the server, the client sends all of its requests to the proxy. The proxy then opens a connection to the server, and passes on the client's request. The proxy receives the reply from the server, and then sends that reply back to the client. Notice that the proxy is essentially acting like both an HTTP client (to the remote server) and an HTTP server (to the initial client).

Why use a proxy? There are a few possible reasons:

*   **Performance:** By saving a copy of the pages that it fetches, a proxy can reduce the need to create connections to remote servers. This can reduce the overall delay involved in retrieving a page, particularly if a server is remote or under heavy load.
*   **Content Filtering and Transformation:** While in the simplest case the proxy merely fetches a resource without inspecting it, there is nothing that says that a proxy is limited to blindly fetching and serving files. The proxy can inspect the requested URL and selectively block access to certain domains, reformat web pages (for instances, by stripping out images to make a page easier to display on a handheld or other limited-resource client), or perform other transformations and filtering.
*   **Privacy:** Normally, web servers log all incoming requests for resources. This information typically includes at least the IP address of the client, the browser or other client program that they are using (called the User-Agent), the date and time, and the requested file. If a client does not wish to have this personally identifiable information recorded, routing HTTP requests through a proxy is one solution. All requests coming from clients using the same proxy appear to come from the IP address and User-Agent of the proxy itself, rather than the individual clients. If a number of clients use the same proxy (say, an entire business or university), it becomes much harder to link a particular HTTP transaction to a single computer or individual.


## Part A: HTTP Proxy

### Getting Started
* On your host machine (laptop), go to the course directory.
```bash
$ cd COS461-Public/assignments
```

* Now, pull the latest update from Github.
```bash
$ git pull
```

* Reprovision your VM as follows:
```bash
$ vagrant reload --provision
```

* SSH to the VM:
```bash
$ vagrant ssh
```

* You will find the following starter code files in the /vagrant/assignment7 directory in the VM:
```
Makefile       http_proxy.go       http_proxy_DNS.go        test_scripts        README.md      src
```

### Task Specification

Your task is to build a web proxy capable of accepting HTTP requests, forwarding requests to remote (origin) servers, and returning response data to a client.

The proxy will be implemented in Go in the file `http_proxy.go`.   **You are allowed and encouraged to use the Go `net` and `net/http` libraries**, documentation here: https://golang.org/pkg/net/ & https://golang.org/pkg/net/http/. Understanding and properly using these libraries will make this assignment much simpler.  

HTTP is an application layer protocol that operates on top of TCP. This allows you to program at multiple levels of abstraction, because all of HTTP is simply part of the "content" of TCP packets.  The `net` library contains socket programming functions and types that operate at the transport layer (TCP). The `net` library functions are more general, requiring more code overall and  manual creation of HTTP message strings, but they are more flexible and more clearly documented. The `http` library contains functions and types that operate at the HTTP application layer.  The `http` library functions are more specific to HTTP, potentially letting you use fewer lines of code, but they are less flexible (and the documentation is more difficult to understand). 

Our reference solution uses the `Request` type and associated functions from the `http` library for parsing and modifying HTTP requests, but uses the `Listen()`, `Accept()`, and `Dial()` functions from `net` (rather than the various server and client functions in `http`). This reference implementation is approximately 130 lines.  How you ultimately decide to combine the `net` and `http` libraries to implement your proxy is up to you. Your grade will not be affected by implementation choices that do not affect the behavior of your proxy.

Your proxy should compile without errors on the course VM using the provided `Makefile`.  Compilation should produce a binary called `http_proxy` that takes as its first argument a port to listen from. Don't use a hard-coded port number.

You shouldn't assume that your proxy will be running on a particular IP address, or that clients will be coming from a pre-determined IP address.

#### Getting Requests from Clients

Your proxy should listen on the port specified from the command line and wait for incoming client connections. See the linked Go sockets documentation from Assignment 1 for more on socket programming in Go.   Client requests should be handled concurrently, with a new [goroutine](https://tour.golang.org/concurrency/1) spawned to handle each request.

Once a client has connected, the proxy should read data from the client and then check for a properly-formatted HTTP request. Use the  `http` library to ensure that the proxy receives a request that contains a valid request line.

Your proxy is only responsible for the GET method. All other request methods should elicit a well-formed HTTP response with status code 500 "Internal Error".  This Wikipedia article has a full list of valid HTTP status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes.  You probably won't need to return status 418 "I'm a teapot"...

#### Sending Requests to Servers

Once the proxy has parsed the URL in the client request, it can make a connection to the requested host (using the appropriate remote port, or the default of 80 if none is specified) and send the HTTP request for the appropriate resource. The proxy should always send the request in the relative URL + Host header format regardless of how the request was received from the client.  

For example, if the proxy accepts the following request from a client:

```
GET http://www.princeton.edu/ HTTP/1.1
```

It should send the following request to the remote server:

```
GET / HTTP/1.1
Host: www.princeton.edu
Connection: close
(Additional client specified headers, if any...)
```

Note that we always send HTTP/1.1 flags and a `Connection: close` header to the server, so that it will close the connection after its response is fully transmitted, as opposed to keeping open a persistent connection. So while you should pass the client headers you receive on to the server, you should make sure you replace any `Connection` header received from the client with one specifying `close`, as shown. To add new headers or modify existing ones, use the `http` library Request type.

#### Returning Response to Clients

After the response from the remote server is received, the proxy should send the response message as-is to the client via the appropriate socket. To be strict, the proxy would be required to ensure a `Connection: close` is present in the server's response to let the client decide if it should close its end of the connection after receiving the response. However, checking this is not required in this assignment because a well-behaving server would respond with a `Connection: close`  given that we ensure that the proxy sends the server a close token.


#### Status Codes from Proxy to Client
For any error caught by the proxy, the proxy should return the status 500 'Internal Error'. As stated above, any request method other than GET should cause your proxy to return status 500 'Internal Error' rather than 501 'Not Implemented'. Likewise, for any invalid, incorrectly formed headers or requests, your proxy should return status 500 'Internal Error' rather than 400 'Bad Request' to the client.

Otherwise, your proxy should simply forward status replies from the remote server to the client. This means most 1xx, 2xx, 3xx, 4xx, and 5xx status replies should go directly from the remote server to the client through your proxy. (While you are debugging, make sure that 404 status replies from the remote server are not the result of poorly forwarded requests from your proxy.)


### Testing Your Proxy

Run your proxy with the following command:

`./http_proxy <port> &`, where `port` is the port number that the proxy should listen on. As a basic test of functionality, try requesting a page using telnet (don't forget to press enter twice):

```
telnet localhost <port>
Trying 127.0.0.1...
Connected to localhost.localdomain (127.0.0.1).
Escape character is '^]'.
GET http://www.example.com/ HTTP/1.1
```

If your proxy is working correctly, the headers and HTML of example.com should be displayed on your terminal screen. Notice here that we request the absolute URL (`http://www.example.com/`) instead of just the relative URL (`/`). A good sanity check of proxy behavior would be to compare the HTTP response (headers and body) obtained via your proxy with the response from a direct telnet connection to the remote server. Additionally, try requesting a page using telnet concurrently from two different shells.


Then try testing your proxy with the supplied `test_proxy.py`  script.  This will compare the result of fetching 3 pre-determined websites directly versus through your proxy:
```
python test_scripts/test_proxy.py http_proxy  <port (optional, will be random if omitted)>
```

Once you have passed all 4 tests in `test_proxy.py`, try the `test_proxy_conc.py` script. This will test your proxy with different numbers of concurrent client connections.  
```
python test_scripts/test_proxy_conc.py http_proxy  <port (optional, will be random if omitted)>
```

For a slightly more complex test, you can configure Firefox to use your proxy server as its web proxy as follows:

1. Run your proxy on port 12000.
2. On your host machine, open Firefox
3.  Go to 'Preferences'. Select 'Advanced' and then select 'Network'.
4.  Under 'Connection', select 'Settings...'.
5.  Select 'Manual Proxy Configuration'. Remove the default 'No Proxy for: localhost 127.0.0.1.' 
6. Under "HTTP Proxy" enter the hostname (127.0.0.1) and port (12000) where your proxy program is running.
6.  Save your changes by selecting 'OK' in the connection tab and then select 'Close' in the preferences tab.


## Part B: Proxy Optimization by DNS Prefetching 

DNS prefetching is a technique whereby a web proxy resolves domain names for links embedded in an HTTP response before a user clicks on any of the links. This improves page load time by bringing the DNS entries for those links into the cache of the DNS resolver closest to the proxy.   DNS prefetching relies on a simple prediction: If a user asks for a particular page, the chances are good that he or she will next request a page linked to from that page. 

### Task Specification

Your task is to add DNS prefetching to the proxy you implemented in Part A.  First, make a copy of your proxy called `http_proxy_DNS.go`:
```
cp http_proxy.go http_proxy_DNS.go
```
You should implement DNS prefetching in this new file. **Leave the original proxy unedited**  because you will need to submit both. In the new copy, change the filename in the header to "http_proxy_DNS.go".

In order to find the links in the response from remote server, you will need to parse the HTML content.  The `net/html` library contains functions for tokenizing html: https://godoc.org/golang.org/x/net/html.  Find all of the `href`attributes of the `<a>` tags in the HTML that start with "http".  Then issue DNS queries for each using the `LookupHost()` function in the `net` library.  Parsing HTML and sending DNS queries should happen in new goroutines so to not slow down the return of the response to the client. 

Note that you don't need to do anything with the DNS responses.  Merely having sent them will have populated the cache of the DNS resolver. 

As before, your DNS prefetching proxy should compile without errors on the course VM using the provided `Makefile`.  Compilation should produce a binary called `http_proxy_DNS` that takes as its first argument a port to listen from. Don't use a hard-coded port number. You shouldn't assume that your proxy will be running on a particular IP address, or that clients will be coming from a pre-determined IP address.

### Testing Your DNS Prefetching Proxy

Test your DNS prefetching proxy the same way as you tested your original proxy.  When using the test scripts, just change the first command line argument:
```
python test_scripts/test_proxy.py http_proxy_DNS  <port (optional, will be random if omitted)>
python test_scripts/test_proxy_conc.py http_proxy_DNS  <port (optional, will be random if omitted)>
```
You will not notice any speedup on these tests, because they do not access additional websites through links. 

In addition, you can use Wireshark to verify that the proxy is performing DNS lookups correctly.

Finally, try using your new `http_proxy_DNS` with Firefox as before. You will hopefully notice that it is faster to load pages accessed through links on the current page.  However, the magnitude of the speedup that you see depends on your local DNS resolver and the speed of your network connection, so don't be surprised if it is not noticeable. 

## Submission & Grading

You should submit your `http_proxy.go` and `http_proxy_DNS.go` files to the CS dropbox here: https://dropbox.cs.princeton.edu/COS461_S2019/Assignment-7-HTTP-Proxy.

**Put your and your partner's names and netids in comments at the top of both submitted files.**

We will test your proxies by running the `test_proxy.py` and `test_proxy_conc.py` scripts and by performing a few additional tests with different websites and numbers of concurrent clients. 
