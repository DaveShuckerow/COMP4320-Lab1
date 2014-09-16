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

OUTPUT_STRING = """
Response: 
	Size:	{0} bytes
	Request ID:	{1}
	Response:	{2}
"""

from socket import *
import struct, sys

class ClientUDP:
	requestNumber = 0
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = self.connectToServer((host, port))

	def connectToServer(self,addr):
		"""
		Connect to a server over UDP.
		"""
		sock = socket(AF_INET, SOCK_DGRAM)
		sock.connect(addr)
		return sock

	def vowelLength(self, s):
		"""
		Send a string to a remote server.
		Receive its vowel length in return.
		"""
		self.sendMessage(85,s)

		response = receiveMessage(6)
		rtml, rrid, rans = struct.unpack('!hhh',response)

		return rtml, rrid, rans

	def disemvowel(self, s):
		"""
		Send a string to a remote server.
		Receive its disemvowelment in return.
		"""
		sendMessage(170,s)

		response = receiveMessage(4)
		rtml, rrid = struct.unpack('!hhh',response)
		# Receive disemvoweled string
		rans = receiveMessage(sock, rtml-4)

		return rtml, rrid, rans

	def sendMessage(self, op, s):
		tml = 5+len(s)
		rid = requestNumber = requestNumber+1
		header = struct.pack('!hhb',tml,rid,op)
		message = str(header) + s
		
		# Send the message
		self.sock.send(message)

	def receiveMessage(self, responseLen):
		response = bytearray()
		bytesReceived = len(response)
		while bytesReceived < responseLen:
			response.extend(self.sock.recv(responseLen))
			bytesReceived = len(response)
		return response

if __name__ == '__main__':
	try:
		client, host, port, op, s = sys.argv
		port = int(port)
		op = int(op)
		client = ClientUDP(host, port)
		if op == 85:
			result = client.vowelLength(s)
		elif op == 170:
			result = client.disemvowel(s)
		print OUTPUT_STRING.format(result)
	except Exception as e:
		print e