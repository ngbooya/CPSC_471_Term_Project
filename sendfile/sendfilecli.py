
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# from sendfileserv import list_of_file

# Command line checks
if len(sys.argv) < 2:

	print("USAGE python ", sys.argv[0], "<FILE NAME>")

# Server address
# serverAddr = "localhost"
serverAddr = sys.argv[1]

# Server port
# serverPort = 1234
serverPort = sys.argv[2]
# The name of the file
# fileName = sys.argv[1]
# fileName = "file.txt"

# Open the file
# fileObj = open(fileName, "r")


list_of_files = {}





# Keep sending until all is sent
def sendfile(send_file):
	# Create a TCP socket
	connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	connSock.connect((serverAddr, int(serverPort)))

	# Open the file
	fileObj = open(send_file, "r")
	# The number of bytes sent
	numSent = 0

	# The file data
	fileData = None
	while True:

		# Read 65536 bytes of data
		fileData = fileObj.read(65536)

		# Make sure we did not hit EOF
		if fileData:

			# Get the size of the data read
			# and convert it to string
			dataSizeStr = str(len(fileData))

			# Prepend 0's to the size string
			# until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr


			# Prepend the size of the data to the
			# file data.
			fileData = dataSizeStr + fileData

			# The number of bytes sent
			numSent = 0

			# Send the data!
			while len(fileData) > numSent:
				numSent += connSock.send(fileData[numSent:].encode('utf-8'))

		# The file has been read. We are done
		else:
			break

	print("Send", numSent, " bytes")
	connSock.close()
	fileObj.close()


def recvFile(filename):
	# # Create a TCP socket
	# connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#
	# # Connect to the server
	# connSock.connect((serverAddr, int(serverPort)))
	#
	# connSock.send(filename.encode('utf-8'))
	#
	# downloadDir = "./"
	# with open(os.path.join(downloadDir.encode('utf-8'), filename.encode('utf-8')), 'wb') as file_to_write:
	# 	while True:
	# 		data = connSock.recv(1024)
	# 		if not data:
	# 		    break
	# 		file_to_write.write(data.decode('utf-8'))
	# file_to_write.close()
	# connSock.close
	# Create a TCP socket
	connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	connSock.connect((serverAddr, int(serverPort)))

	connSock.send(filename.encode('utf-8'))
	data = connSock.recv(1024)
	print (data.decode('utf-8'))
	list_of_files[filename] = data.decode('utf-8')
	
	connSock.close()

def listFiles():
	# Create a TCP socket
	connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	connSock.connect((serverAddr, int(serverPort)))

	files = connSock.recv(1024).decode('utf-8')
	print(files)
	# if len(list_of_files) == 0:
	# 	return;
	# for key,val in list_of_files.items():
	# 	print(key,"\t");

userInput = None


while userInput != "quit":
	userInput = input("ftp> ")
	file = ""
	if userInput != "ls" and userInput != "quit":
		command,file = userInput.split(" ")
	if userInput == "ls":
		command = "ls"
	if userInput == "quit":
		command = "quit"

	commandSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	commandSock.connect((serverAddr, int(serverPort)))
	

	commandSock.send((command + " " + file).encode('utf-8'));
	commandSock.close();
	# result = commandSock.recv(1024).decode('utf-8')
	# print(result);
	if command == "get":
		print("GET COMMAND")
		recvFile(file)
	elif command == "put":
		print("PUT COMMAND")
		sendfile(file)
	elif command == "ls":
		listFiles()
		print("LS COMMAND")
	elif command == "quit":
		print("QUIT COMMAND")
		print("Goodbye!")





# print("Send", numSent, " bytes")

# Close the socket and the file
# connSock.close()
# fileObj.close()
