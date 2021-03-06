#!/usr/bin/python
"""
ClientTCP.py
Author:	David Shuckerow (djs0017@auburn.edu)
Date:	9/16/2014

String Processing client that supports
	two operations:
		Vowel Length of String
		Disemvoweling of String
"""

OUTPUT_STRING = """Response: 
	Size:		{0} bytes
	Request ID:	{1}
	Answer:		{2}
"""

from socket import *
import struct, sys

class ClientTCP:
	requestNumber = 0
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = self.connectToServer((host, port))

	def connectToServer(self,addr):
		"""
		Connect to a server over TCP.
		"""
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect(addr)
		return sock

	def vowelLength(self, s):
		"""
		Send a string to a remote server.
		Receive its vowel length in return.
		"""
		self.sendMessage(85,s)

		response = self.receiveMessage(1024)
		rtml, rrid, rans = struct.unpack('!HHH',response[:6])

		return rtml, rrid, rans

	def disemvowel(self, s):
		"""
		Send a string to a remote server.
		Receive its disemvowelment in return.
		"""
		self.sendMessage(170,s)

		response = self.receiveMessage(1024)
		rtml, rrid = struct.unpack('!HH',response[:4])
		# Receive disemvoweled string
		rans = response[4:]

		return rtml, rrid, rans

	def sendMessage(self, op, s):

		tml = 5+len(s)
		rid = ClientTCP.requestNumber = ClientTCP.requestNumber+1
		header = struct.pack('!HHB',tml,rid,op)
		message = str(header) + s
		
		# Send the message
		self.sock.sendall(message)

	def receiveMessage(self, responseLen):
		response = self.sock.recv(responseLen)
		return response

if __name__ == '__main__':
	client, host, port, op, s = sys.argv
	port = int(port)
	op = int(op)
	client = ClientTCP(host, port)
	if op == 85:
		print "How many vowels are in \"{}\"?".format(s)
		result = client.vowelLength(s)
	elif op == 170:
		print "Disemvowel the string \"{}\".".format(s)
		result = client.disemvowel(s)
	print OUTPUT_STRING.format(result[0], result[1], result[2])
