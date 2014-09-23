/*
** client.c -- a stream socket client demo
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include <arpa/inet.h>

#define PORT "5555" // the port client will be connecting to 

#define MAXDATASIZE 2048 // max number of bytes we can get at once 

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{
    int sockfd, numbytes;  
    char buf[MAXDATASIZE];
    struct addrinfo hints, *servinfo, *p;
    int rv;
    char s[INET6_ADDRSTRLEN];

    if (argc != 5) {
        fprintf(stderr,"usage: client hostname port operation message\n");
        exit(1);
    }

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;

    if ((rv = getaddrinfo(argv[1], argv[2], &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    // loop through all the results and connect to the first we can
    for(p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                p->ai_protocol)) == -1) {
            perror("client: socket");
            continue;
        }

        if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("client: connect");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "client: failed to connect\n");
        return 2;
    }
   

    inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
            s, sizeof s);
    printf("client: connecting to %s:%s\n", s, argv[2]);
    
    // Send the message:
    unsigned short tml = 5 + strlen(argv[4]);
    unsigned short rid = 1;
    unsigned char  op = atoi(argv[3]);
    char string[1024];
    string[0] = (unsigned char)(tml >> 8);
    string[1] = (unsigned char)tml;
    string[2] = (unsigned char)(rid >> 8);
    string[3] = (unsigned char)rid;    
    string[4] = op;
    int i=0;
    for (i=0; i<strlen(argv[4]); i++) {
    	string[i+5] = argv[4][i];
    	string[i+6] = '\0';
    }
	
    freeaddrinfo(servinfo); // all done with this structure
    
    if (send(sockfd, string, tml,0)) {
    	printf("TML: %d\n", (string[0] << 8)+string[1]);
    	printf("RID: %d\n", (string[2] << 8)+string[3]);
    	printf("OP:  %d\n", (string[4]));
    	printf("Sent message: %s\n",string+5);
    }
	
    if ((numbytes = recv(sockfd, buf, 1024, 0)) == -1) {
        perror("recv");
        exit(1);
    }

    buf[numbytes] = '\0';
	if (op == 85) {
    	printf("TML: %d\n", (buf[0] << 8)+buf[1]);
    	printf("RID: %d\n", (buf[2] << 8)+buf[3]);
    	printf("Vowel Count:  %d\n", (buf[4] << 8)+buf[5]);
	} else if (op == 170) {
		printf("TML: %d\n", (buf[0] << 8)+buf[1]);
    	printf("RID: %d\n", (buf[2] << 8)+buf[3]);
    	printf("Disemvowelment:  %s\n", buf+4);
	}

    close(sockfd);

    return 0;
}
