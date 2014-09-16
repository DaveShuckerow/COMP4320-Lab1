#!/usr/bin/python
"""
ClientUDP.py
Author:	David Shuckerow (djs0017@auburn.edu)
Date:	9/16/2014

String Processing client that supports
	two operations:
		Vowel Length of String
		Disemvoweling of String
"""

requestNumber = 6
OUTPUT_STRING = """
Response: 
	{0} bytes
	{1} request ID
	{2} vowels found
"""

from socket import *
import struct, sys

def connectToServer(addr):
	"""
	Connect to a server over UDP.
	"""
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.connect(addr)
	return sock

def vowelLength(sock, s):
	"""
	Send a string to a remote server.
	Receive its vowel length in return.
	"""
	global requestNumber
	tml = 5+len(s)
	rid = requestNumber = requestNumber+1
	op  = 85
	header = struct.pack('!hhb',tml,rid,op)
	message = str(header) + s
	
	# Send the message
	sock.send(message)

	# Receive a response
	responseLen = 6
	response = bytearray()
	bytesReceived = len(response)
	while bytesReceived < responseLen:
		response.extend(sock.recv(responseLen))
		bytesReceived = len(response)

	# Return the last 2 bytes of the array
	rtml, rrid, rans = struct.unpack('!hhh',response)
	return rtml, rrid, rans

if __name__ == '__main__':
	try:
		client, host, port, op, s = sys.argv
		port = int(port)
		op = int(op)
		sock = connectToServer(addr=(host, port))
		print OUTPUT_STRING.format(vowelLength(sock, "Hello"))
	except Exception as e:
		print e