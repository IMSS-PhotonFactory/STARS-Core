/*
* STARS2TINE interface library - Entry Point
* Origin 2006-06-30
* Takashi Kosuge Modified By Y.Nagatani
* $Revision: 1.1 $
* $Date: 2010-01-19 02:56:39 $
*/
// Header Files
#ifdef WINDOWS
// #include "stdafx.h"
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tine.h"
#include "starsif.h"
#include "starsfnc.h"
#include <time.h>

#define DEVICE_NAME_BUF_LEN 256
#define PROPERTY_BUF_LEN 256

// Internal Use Only
static STARS_CONNECTION *g_starsPtr;		
char MYNAME[STARS_KFNAME_MAX];		
static char StandbyNode[sizeof(g_starsPtr->rcvfrom)];//Add By Nagatani For Attach Link
clock_t  callbackstart, nowend;
extern int getvalue (char *name, char *rtbuf);
extern int main_sub(char *nodename, char *myaddr);
//
// Function stdevhandler()
//
static void stdevhandler(STARS_CONNECTION *scp,char *rtbuf){
	char Device[DEVICE_NAME_BUF_LEN];
	char Property[PROPERTY_BUF_LEN];
	char stiocDBuf[64000];
	int cc;
	int i;	

	char *ptr = g_starsPtr->rcvto + strlen(MYNAME);
	if(ptr[0]!='.'){
		sprintf(rtbuf,"@%s Er: Bad command or parameter.",scp->rcvmess);
		rtbuf[STARS_MESSAGE_MAX-1]=(char)NULL;
		return;
	}

//help
	if(strcmp(scp->rcvmess, "help")==0){
		strcpy(rtbuf,"@help hello flushdata GetValue GetValuePolling GetServerList GetPropertyList GetPropertyInfo RegisterPolling SetValue StopPolling");
//GetValuePolling
	}else if(strcmp(scp->rcvmess, "GetValuePolling")==0){
		if(getvalue(ptr+1,stiocDBuf)>=0){
			sprintf(rtbuf,"@%s %s",scp->rcvmess,stiocDBuf);
		}else{
			sprintf(rtbuf,"@%s Er: Bad command or parameter.",scp->rcvmess);
		}
	}else if(strcmp(scp->rcvmess, "GetValue")==0){
		if(getvalue(ptr+1,stiocDBuf)>=0){
			sprintf(rtbuf,"@%s %s",scp->rcvmess,stiocDBuf);
		}else{
			sprintf(rtbuf,"@%s Er: Bad command or parameter.",scp->rcvmess);
		}
	}else{
		sprintf(rtbuf,"@%s Er: Bad command or parameter.",scp->rcvmess);
	}
	rtbuf[STARS_MESSAGE_MAX-1]=(char)NULL;
	return;
}

//
// Function stctlhandler()
//
static void stctlhandler(STARS_CONNECTION *scp, char *rtbuf){
	int cc;
	int l;
//help
	if(strcmp(scp->rcvmess, "help")==0){
		strcpy(rtbuf, "@help hello flushdata Standby StandbyReset SyncRun StopPolling Reset");
//flushdata
	}else if(strcmp(scp->rcvmess, "flushdata")==0){
		sprintf(rtbuf,"@%s Ok:",scp->rcvmess);
	}else{
		sprintf(rtbuf,"@%s Er: Bad command or parameter.",scp->rcvmess);
	}
	rtbuf[STARS_MESSAGE_MAX-1]=(char)NULL;
	return;
}

//
// Function: Cause Event Messagetinebrg.PFRING.RNGREADER.device_0.IB RegisterPolling
//
void starseventhandler(char *tinefrom, char *to, char *event, char *retdata){
	char tobuf[STARS_SVRN_MAX];
	char rtbuf[STARS_MESSAGE_MAX];
	sprintf(tobuf,"%s>%s",tinefrom,to);
	sprintf(rtbuf,"%s %s",event,retdata);
#ifdef DEBUG
	printf("S(from=%s to=%s): %s\n", tinefrom,to,rtbuf);
#endif
	stars_send(g_starsPtr,rtbuf,tobuf);
}



//
// Command line args check Function for Main
//
#ifdef LINUX
int checkargs(int argc, char **argv, int *startup, char *startupfile, char *starsserver)
#endif
#ifdef WINDOWS
int checkargs(int argc, char **argv, int *startup, char *startupfile, char *starsserver)
//int checkargs(int argc, _TCHAR **argv, int *startup, char *startupfile, char *starsserver)
#endif
{
	int i;
	int item=0;
	
	for(i=1;i<argc;i++){
		if(strncmp(argv[i],"-",1)==0){
			if(strncmp(argv[i],"--help",6)==0){
#ifdef LINUX
				printf("%s [--help|-myaddr:<client Address>] <Nodename> <Server>\nOption\n\t-myaddr:<client Address> =>Specify your 'client Address'\n",argv[0]);
#endif
#ifdef WINDOWS
				printf("%s [--help|-myaddr:<client Address>] <Nodename> <Server>\nOption\n\t-myaddr:<client Address> =>Specify your 'client Address'\n",argv[0]);
#endif
				exit(0);
			}else if(strncmp(argv[i],"-myaddr:",8)==0){
				strcpy(startupfile,argv[i]+8);
				if(startupfile[8]==(char)NULL){
					printf("Missing <client Address> for -myaddr option.\n");
				}
				*startup=0;
			}else{
				printf("Bad option.(%s)\n",argv[i]);
				exit(-1);
			}
		}else if(item==0){
			if(strlen(argv[i])<=sizeof(MYNAME)-1){
				strcpy(MYNAME,argv[i]);item++;
			}else{
				printf("Sorry. Specify the Stars Client Name within %d characters.\n",sizeof(MYNAME)-1);
				exit(-1);
			}
		}else if(item==1){
			if(strlen(argv[i])<=STARS_SVRN_MAX-1){
				strcpy(starsserver,argv[i]);item++;
			}else{
				printf("Sorry. Specify the Stars Server within %d characters.\n",STARS_SVRN_MAX-1);
				exit(-1);
			}
		}else{
			printf("Show help with option --help\n");
			exit(-1);
		}
	}
	return(0);
}


//
// Main Function: Entry Point
//
#ifdef LINUX
int main(int argc, char* argv[])
#endif
#ifdef WINDOWS
int main(int argc, char* argv[])
//int _tmain(int argc, _TCHAR* argv[])
#endif
{
	char keyfile[sizeof(MYNAME)+4];
	char startupfile[sizeof(MYNAME)+8];
	char starsserver[STARS_SVRN_MAX];
	char rtbuf[STARS_MESSAGE_MAX+50];
	int startup=-1;
	float calctime=0;


	strcpy(startupfile,"");
	strcpy(MYNAME,"Ring");			// default stars nodename
	strcpy(starsserver,"localhost");	// default stars server

	// check args: error then exit
	checkargs(argc, argv, &startup, startupfile, starsserver);
	
	StandbyNode[0]=(char)NULL;

	/* Open connection of STARS. "stars_open" tries connection first then allocates
	memories for structure of STARS_CONNECTION. */
	strcpy(keyfile,MYNAME);strcat(keyfile,".key");
//	printf("Accessing Stars Server %s As %s\n",starsserver,MYNAME);
	if((g_starsPtr = stars_open(MYNAME, starsserver, 6057, keyfile))
	  == NULL){exit(-1);}

	// Initialize
	callbackstart = clock();

	main_sub(MYNAME, startupfile);

//  stars_set_timeout(g_starsPtr,STARS_SETTIMEOUTMAX);

//	fprintf(stderr,"Normally startup.\n");

	int run=1;
	while(run == 1){
#ifdef DEBUG
				//printf("run\n");
#endif
		while(stars_receive(g_starsPtr)!=0){
			// Event Or Reply Message Do Nothing
			if((g_starsPtr->rcvmess[0] == '_') || (g_starsPtr->rcvmess[0] == '@')){
			  //_quit	
				if(strcmp(g_starsPtr->rcvmess,"_quit")==0){
					run = 0;
					break;
			  //_quit	
				}else if(strcmp(g_starsPtr->rcvmess,"_exit")==0){
					run = 0;
					break;
				}
			}else{
#ifdef DEBUG
				printf("R(from=%s to=%s): %s\n", g_starsPtr->rcvfrom, g_starsPtr->rcvto, g_starsPtr->rcvmess);
#endif
			  //hello
				if(strcmp(g_starsPtr->rcvmess, "hello")==0){
					strcpy(rtbuf, "@hello nice to meet you.");
			  //disconnect
				}else if(strcmp(g_starsPtr->rcvmess,"disconnect")==0){
					run = 0;
					strcpy(rtbuf, "@disconnect Ok:");
			  //quit
				}else if(strcmp(g_starsPtr->rcvmess,"quit")==0){
					run = 0;
					strcpy(rtbuf, "@quit Ok:");
			  //exit
				}else if(strcmp(g_starsPtr->rcvmess,"exit")==0){
					run = 0;
					strcpy(rtbuf, "@exit Ok:");
			  //Controller	
				}else if(strcmp(g_starsPtr->rcvto,MYNAME)==0){
					stctlhandler(g_starsPtr,rtbuf);
			  //device
				}else{
					stdevhandler(g_starsPtr,rtbuf);
				}
#ifdef DEBUG
				printf("S(from=%s to=%s): %s\n", g_starsPtr->rcvto, g_starsPtr->rcvfrom, rtbuf);
#endif
				//stars_send(scp, rtbuf, scp->rcvfrom);
				//These 3 lines can support hierarchical structure instead of previous one.
				strcat(g_starsPtr->rcvto, ">");
				strcat(g_starsPtr->rcvto, g_starsPtr->rcvfrom);
				stars_send(g_starsPtr, rtbuf, g_starsPtr->rcvto);
				if(run != 1){
					break;
				}
			}
		}
	    SystemCycle(TRUE);

   		nowend = clock();
   		calctime= (float)(nowend-callbackstart)/ CLOCKS_PER_SEC;
   		if(calctime > 60){
			printf("No Reply from TINE Server :%-12.4f seconds\n", calctime );
			break;
   		}

	}
#ifdef DEBUG
				//printf("quit\n");
#endif
	_SystemReset(0);   
#ifdef WINDOWS
	//close(g_starsPtr->handle);
	stars_free(g_starsPtr);
#else
	stars_close(g_starsPtr);
#endif
	exit(0);
}
