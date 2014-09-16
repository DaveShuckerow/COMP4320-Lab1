#!/usr/bin/python
"""
ServerTCP.py
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

class ServerTCP:
	def __init__(self, port):
		self.host = ''
		self.port = port
		self.sock = self.setupServer()
		self.runServer()

	def setupServer(self):
		sock = socket(AF_INET, SOCK_STREAM)
		sock.bind((self.host, self.port))
		sock.listen(1)
		return sock

	def runServer(self):
		while True:
			conn, addr = self.sock.accept()
			print "Received connection from {}".format(addr)
			header = self.receiveMessage(conn, 5)
			tml, rid, op = struct.unpack("!HHB", header)
			s = str(self.receiveMessage(conn, tml-5))
			print "Request: {0} {1} {2} {3}".format(tml, rid, op, s)
			ans = 0
			if op == 85:
				ans = self.countVowels(conn, s)
			elif op == 170:
				ans = self.disemvowel(conn, s)
			rtml = 4+len(ans)
			print "Answer: {0} {1} {2}".format(rtml, rid, ans)
			response = str(struct.pack("!HH", rtml, rid)) + ans
			conn.sendall(response)
			conn.close()

	def countVowels(self, conn, s):
		count = 0
		for c in s:
			if c in VOWELS:
				count += 1
		answer = struct.pack("!H", count)
		return str(answer)

	def disemvowel(self, conn, s):
		answer = ""
		for c in s:
			if c not in VOWELS:
				answer += c
		return answer

	def receiveMessage(self, conn, responseLen):
		response = bytearray()
		bytesReceived = len(response)
		while bytesReceived < responseLen:
			response.extend(conn.recv(responseLen))
			bytesReceived = len(response)
		return response

if __name__ == '__main__':
	port = int(sys.argv[1])
	server = ServerTCP(port)