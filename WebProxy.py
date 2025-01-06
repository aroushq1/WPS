from socket import *
import os

# Create a server socket, bind it to a port and start listening
proxyServerPort = 8888
proxySerSock = socket(AF_INET, SOCK_STREAM) #TCP
proxySerSock .bind(('',proxyServerPort)) #welcoming socket
proxySerSock .listen(1) #server listens for TCP connection requests from the client, parameter specifies the maximum number of queued connections (at least 1)

while 1:
    print('Ready to serve...')
    #accept connection from clients
    proxyAsClientSocket, addr = proxySerSock.accept() #establishing conenction
    print('Received a connection from:', addr)

    # get the http request from client
    message = proxyAsClientSocket.recv(2048).decode() 
    print(message)

    # if message is not a GET request send a response 400 Bad request to the client
    #close the connection and go to the next iteration of while loop waiting for another request
    #from the same or a different client
    if not message.startswith("GET"):
        print("message is not a GET")
        # fill in start.
        response = "HTTP/1.0 400 Bad Request \r\n\r\n"
        proxyAsClientSocket.send(response.encode()) #sending response message to client
        proxyAsClientSocket.close()  
        continue

    # Extract the pathname(including the filename) and hostname from the given message
    slashPlusUrl = message.split()[1]
    # fill in start
    url = slashPlusUrl.partition("/")[2]
    hostn = url.split('/', 1)[0]
    pathname = "/" + url.split('/', 1)[1]
    # fill in end.

    # remove "www." from the hostname if it starts with "www."
    if hostn.startswith("www."):
        hostn = hostn.replace("www.", "", 1)

    print("pathname: " , pathname)
    print("hostname: ", hostn)

    fileExist = "false"

    directory = "./" + url

    try:
        # Check whether the file exist in the cache using open() method
        # If file exists it opens file and reads otherwise it throws as exception
        f = open(directory, "rb")
        object = f.read()

        # Send http response header and object
        responseHeader = "HTTP/1.0 200 OK\r\nConnection: close\r\n\r\n" 
        proxyAsClientSocket.send(responseHeader.encode() + object)
        fileExist = True
        print('Read from cache')

        #close socket and file
        proxyAsClientSocket.close() #closing socket
        f.close() #closing file

    except IOError: # Error handling for file not found in cache

        if fileExist == "false":
            # Create a socket on the proxyserver to connect to the original server on port 80
            proxyAsClientSocket = socket(AF_INET, SOCK_STREAM) #TCP
            proxyAsClientSocket.connect((hostn,80)) # Connect to the original server on port 80

            #create a get request message and send the message to the server using the socket just created in above lines
            # Hint : use pathname and hostn in the request message

            #fill in start
            getRequest = f"GET {pathname} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
            proxyAsClientSocket.send(getRequest.encode()) 
            #fill in end

            # initialize response to empty in binary format - works for any type of document
            total_response = b''

            # receive data from web server
            #Hint: You can use a while loop and get response in chunks until it is finished.
            #Fill in start
            while True:
                responseChunk = proxyAsClientSocket.recv(4096)
                if not responseChunk:
                    break
                total_response += responseChunk
            #Fill in end

            #Separate header and object
            #Hint use split function. Check the lecture notes to see what separates the response header and object
            response_header = total_response.split(b"\r\n\r\n", 1)[0]
            response_object = total_response.split(b"\r\n\r\n", 1)[1]


            if b'200 OK' in response_header:
                # if the response is a 200 OK response create the directory and file and write the object into the file
                # Then, send http response header and object to the client
                #Fill in start
                os.makedirs(os.path.dirname(directory), exist_ok=True)
                with open(directory, "wb") as cache_file:
                    cache_file.write(response_object)
                proxyAsClientSocket.send(response_header + b"\r\n\r\n" + response_object) # Sending HTTP response header and object to client
                #Fill in end
            else:
                #Otherwise, i.e., if response is not a 200 OK message,send 400 bad response
                #Fill in start
                response = "HTTP/1.0 400 Bad Request \r\n\r\n"
                proxyAsClientSocket.send(response.encode()) #sending bad response message to client
                #Fill in end

            # close socket between proxy and origin server
            proxyAsClientSocket.close()
        else:
            break
    except:
        print("An Exception Occurred")
    finally:
        # close socket between proxy and client
        proxyAsClientSocket.close()
    break #to test file with multiple objects. If the tested URLs have only one object you can remove "break"


#close the main proxy listening socket
proxySerSock.close()
print("finish")
