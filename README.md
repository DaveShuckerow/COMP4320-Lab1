Intro to Computer Networks Project 1
====================================

Part A: Datagram socket programming  
------------------------------------
The objective is to design a **String Processing Server (SPS)**. This SPS operates string operations as requested by a client. Your server must offer two operations: 
	1) number of voyels (`vLength`) in a string and 
	2) String Disemvoweling. 
1) 'vLength' of a string:
 	* A client will send a string S to the server, and the server will return the number of voyels in S. The client sends a message with the following format:
		Total Message Length (TML): 2 bytes
		Request ID: bytes
		Operation: 1 byte
		String: Variable
	* Total Message Length (TML) is an integer representing the total numbers of bytes making the message including TML. Request ID is an integer representing the request ID. This will allow a client to distinguish its requests. Operation is the operation requested (85 (0x55) for vLength and 170 (0xAA) for Disemvoweling) String is the string parameter

	* Example: suppose the Client requests for the length of sentence "Hello", the message will contain (if this is the 7th request): `0x00 0x0A 0x00 0x07 0x55 0x48 0x65 0x6C 0x6C 0x6F`.  The Server will respond with a message with this format:
		Total Message Length (TML): 2 bytes
		Request ID: 2 bytes
		Answer (Length): 2 bytes

	* Example: the server will respond to the 7th request (example above) with: `0x00 0x0A 0x00 0x07 0x00 0x02`
2) String Disemvoweling:
	*The Client will send a request with the following format
		Total Message Length (TML): 2 bytes
		Request ID: bytes
		Operation: 1 byte
		String: Variable                         
	* The meaning of the fields is the same as for requesting the length (see above). The only difference is that the Operation field will contain the value `0xAA`. Example: suppose the Client needs to disemvowel the sentence "Hello", the message will contain (if this is the 8th request): `0x00 0x0A 0x00 0x08 0xAA 0x48 0x65 0x6C 0x6C 0x6F`  The server answers with a packet with this form:
		Total Message Length (TML): 2 bytes
		Request ID: 2 bytes
		String: Variable
	* Example: The server will respond to the  8th request with: `0x00 0x07 0x00 0x08 0x48 0x4C 0x4C`
a) **Repetitive Server**: Write a datagram **String Processor server (ServerUDP.c)**. This program must be written in C. This server must respond to requests as described above. The server must run on port `(10010+GID)` and could run on any machine on the Internet. GID is your group ID. The server must accept a command line of the form: *server portnumber* where *portnumber* is the port where the server should be working.
b) Write a datagram **client (ClientUDP.xx)** in ANY language other
than C or C++ which:

	i. Accepts as command line of the form: client servername
	PortNumber Operation String where servername is the server name, PortNumber  is the port number, Operation  is the operation requested (85 for length and 170 for Disemvoweling), and String  is the string.
	ii. forms a message as described above
	iii. Sends the message to the server and waits for a response
	iv. Prints out the response of the server: the request ID and the response
	v. Prints out the round trip time (time between the transmission of the request and the reception of the response)

Part B: TCP socket programming
------------------------------
Repeat part A using TCP sockets to produce (ServerTCP.xxx, ClientTCP.c). The client must be written in C. The server must be written in any language other than C or C++.

Grading:
--------
1) 25 points per program (2 clients and 2 servers) 
2) Code does not compile on Tux machine:  0% credit 
3) Code compiles on Tux machines but does work: 5% credit 
4) Code compiles and interacts correctly with counterpart from the same group: 70% credit 
5) Code compiles and interacts correctly with counterpart from other groups: 100% credit


Advice to complete these exercises:
-----------------------------------
This is just an introduction to socket programming: I advise to work ACTIVELY to implement these programs.
Step 1: download, compile, and execute Beej’s sample programs for Section 6.3 (talker.c
(client) and listener.c (server)) Step 2: get familiar with this code: study key socket programming calls/methods/functions Step 3: improve the server to echo (send back) the string it received. Step 4: improve the client to receive the echo and print it out. Step 5: SAVE the improved versions (you may need to roll back to them when things will go bad) Step 6: All you need now is “forming” your messages based on the specified format. For the TCP socket programming, redo Step 1-6 using Beej’s stream sample programs
(Sections 6.1-6.2)


What to turn in?
----------------
1) Hard copy of your lab report (with the code)  with group id, students names and email addresses. 
2) Electronic copy of your report and code. These sources codes named as shown above and your report must me put in a folder named lab1XX where XX is your group ID (on Canvas) by only one of the groupmates. **Zip the folder and post it on Canvas**. Failing to submit the proper format will result in 25% penalty. 
3) Your code MUST compile and execute on engineering machines tuxXYZ 
4) Your report must:
	a. state whether your code works 
	b. explain the TA how to compile and execute your code 
	c. Responses when applicable (quality of writing and presentation will greatly affect your final grade when your responses are correct). 
	d. report bugs/problems

If the TA is unable to access/compile/execute your work, no credit will be awarded. If the turnin instructions are not followed, 25 pts will be deducted.