/*************************************************************************
Sample program of STARS client. 2006-02-07 Takashi Kosuge

This sample is primitive user client.
**************************************************************************/

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<starsif.h>
#include<starsfnc.h>

#define DESTINATION "icsample"


int main(void){
	STARS_CONNECTION *svr1;
	char msgbuf[256];
/* Open connection of STARS. "satars_open" tries connection first then allocates
memories for structure of STARS_CONNECTION. */
	if((svr1 = stars_open("ucsample", "localhost", 6057, "ucsample.key"))
	  == NULL){exit(-1);}

	printf("Input command for %s.\n", DESTINATION);

	while(scanf("%s", msgbuf) != EOF){

		stars_send(svr1, msgbuf, DESTINATION); /* Send message to destination client */

		/* raad message if sent message is "command". */
		if((msgbuf[0] != '@') && (msgbuf[0] != '_')){
			stars_receive(svr1);
			printf("R(from=%s to=%s): %s\n", svr1->rcvfrom, svr1->rcvto, svr1->rcvmess);
		}

	}

	stars_close(svr1);
}

