#!/usr/bin/python
"""
ServerUDP.py
Author:	David Shuckerow (djs0017@auburn.edu)
Date:	9/16/2014

String Processing server that supports
	two operations: 
		Vowel Length of String
		Disemvoweling of String
"""

VOWELS = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]

from socket import *
import struct, sys

class ServerUDP:
	def __init__(self, port):
		self.host = ''
		self.port = port
		self.sock = self.setupServer()
		self.runServer()

	def setupServer(self):
		sock = socket(AF_INET, SOCK_DGRAM)
		sock.bind((self.host, self.port))
		return sock

	def runServer(self):
		while True:
			message, addr = self.sock.recvfrom(2**12)
			print "Received connection from {}".format(addr)
			header = message[:5]
			tml, rid, op = struct.unpack("!HHB", header)
			s = str(message[5:])
			print "Request: {0} {1} {2} {3}".format(tml, rid, op, s)
			ans = 0
			if op == 85:
				ans = self.countVowels(s)
			elif op == 170:
				ans = self.disemvowel(s)
			rtml = 4+len(ans)
			print "Answer: {0} {1} {2}".format(rtml, rid, ans)
			response = str(struct.pack("!HH", rtml, rid)) + ans
			# Send the message
			sent = self.sock.sendto(response, (addr))

	def countVowels(self, s):
		count = 0
		for c in s:
			if c in VOWELS:
				count += 1
		answer = struct.pack("!H", count)
		return str(answer)

	def disemvowel(self, s):
		answer = ""
		for c in s:
			if c not in VOWELS:
				answer += c
		return answer

	def receiveMessage(self, responseLen):
		response = bytearray()
		addr = ''
		bytesReceived = len(response)
		while bytesReceived < responseLen:
			resp, addr = self.sock.recvfrom(responseLen)
			response.extend(resp)
			bytesReceived = len(response)
		return response, addr

if __name__ == '__main__':
	port = int(sys.argv[1])
	server = ServerUDP(port)