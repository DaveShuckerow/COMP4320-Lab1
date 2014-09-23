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

OUTPUT_STRING = """Response: 
	Size:		{0} bytes
	Request ID:	{1}
	Answer:		{2}
"""

from socket import *
import struct, sys, time

class ClientUDP:
	requestNumber = 0
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket(AF_INET, SOCK_DGRAM)

	def vowelLength(self, s):
		"""
		Send a string to a remote server.
		Receive its vowel length in return.
		"""
		self.sendMessage(85,s)

		response, addr = self.sock.recvfrom(2**12)
		rtml, rrid, rans = struct.unpack('!HHH',response[:6])

		return rtml, rrid, rans

	def disemvowel(self, s):
		"""
		Send a string to a remote server.
		Receive its disemvowelment in return.
		"""
		self.sendMessage(170,s)

		response, addr = self.sock.recvfrom(2**12)
		header = response[:4]
		rtml, rrid = struct.unpack('!HH',header)
		# Receive disemvoweled string
		rans = str(response[4:])

		return rtml, rrid, rans

	def sendMessage(self, op, s):
		"""
		Conduct the message sending.
		"""
		tml = 5+len(s)
		rid = ClientUDP.requestNumber = ClientUDP.requestNumber+1
		header = struct.pack('!HHB',tml,rid,op)
		message = str(header) + s
		
		# Send the message
		sent = self.sock.sendto(message, (self.host, self.port))
		while sent < tml:
			sent += self.sock.sendto(message[sent:], (self.host, self.port))

if __name__ == '__main__':
	client, host, port, op, s = sys.argv
	port = int(port)
	op = int(op)
	client = ClientUDP(host, port)
	if op == 85:
		start = time.time()
		print "How many vowels are in \"{}\"?".format(s)
		result = client.vowelLength(s)
		print OUTPUT_STRING.format(result[0], result[1], result[2])
		print "\tRound Trip Time: {}s".format(time.time()-start)
	elif op == 170:
		start = time.time()
		print "Disemvowel the string \"{}\".".format(s)
		result = client.disemvowel(s)
		print OUTPUT_STRING.format(result[0], result[1], result[2])
		print "\tRound Trip Time: {}s".format(time.time()-start)
	else:
		print "--INVALID OPERATION REQUESTED--"
		print "   Use operation 85 or 170"
		print "   to request vowel length"
		print "      or disemvowelment"
	
