#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <ctype.h>

#define BUF_SIZE 1024
const char *vLengthCode = "85";
const char *dVowelCode = "170";
const char *vowels ="aeiouAEIOU";
int count = 0;


int main(int argc, char* argv[]) {
    char buf[BUF_SIZE];
    char temp[BUF_SIZE];
    struct sockaddr_in self, other;
    int len = sizeof(struct sockaddr_in);
    int n, s, port;

    if (argc < 2) {
	fprintf(stderr, "Usage: %s <port>\n", argv[0]);
	return 1;
    }

    /* initialize socket */
    if ((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1) {
	perror("socket");
	return 1;
    }

    /* bind to server port */
    port = atoi(argv[1]);
    memset((char *) &self, 0, sizeof(struct sockaddr_in));
    self.sin_family = AF_INET;
    self.sin_port = htons(port);
    self.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(s, (struct sockaddr *) &self, sizeof(self)) == -1) {
	perror("bind");
	return 1;
    }

    while ((n = recvfrom(s, buf, BUF_SIZE, 0, (struct sockaddr *) &other, &len)) != -1) 
    {
	printf("Received from %s:%d: ", 
		inet_ntoa(other.sin_addr), 
		ntohs(other.sin_port)); 
	fflush(stdout);
    int u = 0;
  while (u < 4) 
  {
    temp[u] = buf[u];
    u++;
  }
	write(1, buf, n);
	write(1, "\n", 1); 
 
    //char *c = buf;
     //while (*c)
   //{
       //if (strchr(vLengthCode, *c))
      if (buf[4] == 85)
       {   
          count = 0;
          int i = 5;
          printf("Hi");
          fflush(stdout);
          while(buf[i] != '\0') 
          {
                if(strchr(vowels, i)) 
                {
                count++;
                }
                i++;
          }   
          buf[1] = count;
          
       }
       //else if (strchr(dVowelCode, *c))
       else if (buf[4] == 170)
       {    
            printf("Hey");
            fflush(stdout);
            int k = 0;
            char noVow[100] = "";
            int j = 1;
            while(buf[j] != '\0') 
            {
                if(!strchr(vowels, j)) 
                {
                noVow[k] = buf[j];
                k++;
                }
                j++;
            }
            // Write to buffer
            int r = 0;
            int t = 1;
            while (noVow != " ")
            {
              buf[t] = noVow[r];
              r++;
              t++;
            }
            
       }
   //    c++;
  // }
  // memcpy (buf, temp, strlen(temp) + 1);
	/* echo back to client */
   
	sendto(s, buf, n, 0, (struct sockaddr *) &other, len);
    }
 
    close(s);
    return 0;
}