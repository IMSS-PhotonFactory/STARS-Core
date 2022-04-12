/*************************************************************************
Sample program of STARS client. 2006-02-07 Takashi Kosuge

Usually STARS I/O client has an event handling function.
**************************************************************************/

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<starsif.h>
#include<starsfnc.h>

int sthandler(STARS_CONNECTION *scp);
int get_rand_value(char *rtbuf);



int main(void){
	STARS_CONNECTION *svr1;

/* Open connection of STARS. "satars_open" tries connection first then allocates
memories for structure of STARS_CONNECTION. */
	if((svr1 = stars_open("icsample", "localhost", 6057, "icsample.key"))
	  == NULL){exit(-1);}

/* "sthandler" will be called when this client receives a message from STARS server. */
	svr1->cbfunc = sthandler;
	stars_add_callback(svr1);

/* Wait for input */
	stars_mainloop(0);

	stars_close(svr1);
}

int  sthandler(STARS_CONNECTION *scp){
	static char rtbuf[STARS_MESSAGE_MAX];

	if(strncmp(scp->rcvmess, "help", 4)==0){
		strcpy(rtbuf, "@help hello GetValue");

	}else if(strncmp(scp->rcvmess, "hello", 5)==0){
		strcpy(rtbuf, "@hello nice to meet you.");

	}else if(strncmp(scp->rcvmess, "GetValue", 8)==0){
		strcpy(rtbuf, "@GetValue ");
		get_rand_value(rtbuf);
	}else if((scp->rcvmess[0] == '_') || (scp->rcvmess[0] == '@')){
		printf("R(from=%s to=%s): %s\n", scp->rcvfrom, scp->rcvto, scp->rcvmess);
		return(0);

	}else{
		strcpy(rtbuf, "@");
		strncat(rtbuf, scp->rcvmess, STARS_MESSAGE_MAX - strlen(rtbuf) - 1);
		strncat(rtbuf, " Er: Bad command or parameter.", STARS_MESSAGE_MAX - strlen(rtbuf) - 1);
	}

	printf("R(from=%s to=%s): %s\n", scp->rcvfrom, scp->rcvto, scp->rcvmess);
	printf("S(from=%s to=%s): %s\n", scp->rcvto, scp->rcvfrom, rtbuf);

	stars_send(scp, rtbuf, scp->rcvfrom);
/* These 3 lines can support hierarchical structure instead of previous one.
	strcat(scp->rcvto, ">");
	strcat(scp->rcvto, scp->rcvfrom);
	stars_send(scp, rtbuf, scp->rcvto);
*/
	return(0);
}

int get_rand_value(char *rtbuf){
	int lp;
	int rt;
	char buf[64];
	for(lp=0; lp<20; lp++){
		if(lp !=0){
			strcat(rtbuf, ",");
		}
		sprintf(buf, "%d",rand());
		strcat(rtbuf, buf);
	}
	return(0);
}
