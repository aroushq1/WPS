# Web Proxy Server

This repository contains the implementation of an HTTP Web Proxy Server in Python. The proxy server operates by accepting connections from HTTP clients (such as web browsers), processing incoming HTTP GET requests, and serving requested resources from a local cache or by fetching them from the origin server.

# Features
Cache Management: Locally stores requested objects to serve future requests from the cache, improving efficiency and reducing latency.

File Naming and Directory Structure: Creates local copies of requested resources using the hostname/pathname of the URL, maintaining the directory structure.

GET Request Handling: Processes well-formed HTTP GET requests. For non-GET requests, the server responds with a 400 Bad Request status.

Response Validation: If the origin server returns a response other than 200 OK, the proxy sends a 400 Bad Request response to the client.

Non-Persistent HTTP Support: Implements HTTP 1.0 by closing the TCP connection after serving each request and includes the Connection: close header in the response.

Text and Binary Support: Handles both text-based resources (e.g., HTML files) and binary resources (e.g., images, PDFs).

# How It Works
Connection Handling: The proxy server listens for client connections and processes HTTP requests.

Local Cache Check: Upon receiving a request, the proxy checks if the requested resource exists in the local cache.

Fetch from Origin Server: If the resource is not cached, the proxy fetches it from the origin server and stores a local copy.

Response to Client: The resource is sent back to the client, either from the cache or directly from the origin server.

# Usage
Run the proxy server and configure your web browser to route traffic through the proxy (using your machine's IP address and the specified port number).

Request web pages through the proxy to verify its functionality.

# Testing
Binary file test:
http://gaia.cs.umass.edu/kurose_ross/programming/Python_code_only/Web_Proxy_programming_only.pdf

Text file test:
http://web.simmons.edu/~grovesd/comm244/notes/week3/html-test-page.html
Deliverables
