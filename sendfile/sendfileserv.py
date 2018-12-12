
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import sys

# The port on which to listen
# listenPort = 1234
list_of_file = {}
listenPort = sys.argv[1]

# Create a welcome socket.
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', int(listenPort)))

# Start listening on the socket
welcomeSock.listen(1)

list_of_files = {}

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************


def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""

	# The temporary buffer
	tmpBuff = ""

	# Keep receiving till all is received
	while len(recvBuff) < numBytes:

		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)

		# The other side has closed the socket
		if not tmpBuff:
			break

		# Add the received bytes to the buffer
		recvBuff += tmpBuff.decode('utf-8')

	return recvBuff

# Accept connections forever
while True:

	# print "Waiting for connections..."
	print("Waiting for Command...")
	commandSock, commandAddr = welcomeSock.accept();
	print("Accepted command connection from client: ", commandAddr)
	command,param = recvAll(commandSock,1024).split(" ")
	print(command,"Param(",param,")")
	# result = "SUCCESS!";
	# commandSock.send(result.encode('utf-8'))
	commandSock.close()

	if command == "ls":
		clientSock, addr = welcomeSock.accept()

		print("Returning File Listing...")
		if len(list_of_files) == 0:
			clientSock.sendall(("ERROR: No Files!").encode('utf-8'))
		else:
			files = ""
			for key,val in list_of_files.items():
				files += key + "\t";
			clientSock.sendall(files.encode('utf-8'))
	elif command == "get":
		print("Returning File Data")
		clientSock, addr = welcomeSock.accept()
		reqFile = clientSock.recv(1024)
		fileName = reqFile.decode('utf-8')
		print("requesting: ", fileName)

		# with open(reqFile.decode('utf-8'), 'rb') as file_to_send:
		# for data in file_to_send:
		if fileName in list_of_files:
			clientSock.sendall(list_of_files[fileName].encode('utf-8'))
		else:
			clientSock.sendall(("ERROR: " + fileName +" not found!").encode('utf-8'))

		# Close our side
		clientSock.close()
	elif command == "put":

		print("Waiting for file.")
		# Accept connections
		clientSock, addr = welcomeSock.accept()

		# print "Accepted connection from client: ", addr
		# print "\n"

		print("Accepted data connection from client: ", addr)
		print("\n")

		# The buffer to all data received from the
		# the client.
		fileData = ""

		# The temporary buffer to store the received
		# data.
		recvBuff = ""

		# The size of the incoming file
		fileSize = 0

		# The buffer containing the file size
		fileSizeBuff = ""

		# Receive the first 10 bytes indicating the
		# size of the file
		fileSizeBuff = recvAll(clientSock, 10)

		# Get the file size
		fileSize = int(fileSizeBuff)

		# print "The file size is ", fileSize
		print("The file size is", fileSize)
		print(fileSizeBuff)

		# Get the file data
		fileData = recvAll(clientSock, fileSize)

		# print "The file data is: "
		# print fileData
		print("The file data is: ")
		print(fileData)

		list_of_files[param] = fileData

		print("Saved to Dictionary: ",param)
		print(list_of_files[param])
		# if (fileData)
		# {
		
		# fileData_tmp = fileData
		# }

		# sock.close()

		# Close our side
		clientSock.close()

	elif command == "quit":
		print("Goodbye!")
		break
		
	


