#include <stdlib.h>
#include <string.h>
#ifndef WINDOWS
#include <math.h>
#endif
#include <time.h>
#include "tine.h"
 
#define DEVSRVNAME "/PFRING/RNGREADER"

#define DOUBLE_NUM 5
#define CHAR_NUM 3
#define ATTACH_NUM 8

double array_double[DOUBLE_NUM];
char array_char[CHAR_NUM][256+2];

double pre_array_double[DOUBLE_NUM];
char pre_array_char[CHAR_NUM][256+2];

typedef struct noname
{
	int id;
	char name[10];
	char starsname[40];
	void *ptr;
	void *preptr;
	int format;
	int size;
} Attach;

extern char MYNAME[];

Attach attachPtr[] =
{-1,"DATETIME","DATETIME",&array_double[0],&pre_array_double[0],CF_DOUBLE,1
,-1,"BEAMCUR" ,"DCCT",&array_double[1],&pre_array_double[1],CF_DOUBLE,1
,-1,"BEAMENE" ,"Energy",&array_double[2],&pre_array_double[2],CF_DOUBLE,1
,-1,"BEAMPAV" ,"Vacuum",&array_double[3],&pre_array_double[3],CF_DOUBLE,1
,-1,"BEAMLIF" ,"Lifetime",&array_double[4],&pre_array_double[4],CF_DOUBLE,1
,-1,"BEAMMOD" ,"Status",&array_char[0],&pre_array_char[0],CF_CHAR,2
,-1,"BEAMMES" ,"Message",&array_char[1],&pre_array_char[1],CF_CHAR,50
,-1,"IDGAP"   ,"IDGap",&array_char[2],&pre_array_char[2],CF_CHAR,256
};

extern int tineDebug;
//extern char gtEthrAddr[];
extern clock_t	callbackstart;
extern void starseventhandler(char *tinefrom, char *to, char *event, char *retdata);

void set_starsnodename ( char *nodename){
  	char buf[256];
    int i;
    for (i=0; i<ATTACH_NUM; i++) {
		strcpy(buf,attachPtr[i].starsname);
		sprintf(attachPtr[i].starsname,"%s%s%s",nodename,".",buf);
	}
	return;
}
int getvalue (char *name, char *rtbuf){
     int i;
  	char buf[256];
  	
	strcpy(buf,MYNAME);
	strcat(buf,".");
	strcat(buf,name);

     for (i=0; i<ATTACH_NUM; i++) {
//     printf("%d %s %s %s",i,attachPtr[i].name,buf,name);
	if(strcmp(attachPtr[i].name,name)==0){
     		if(attachPtr[i].format == CF_DOUBLE){
  	 	        sprintf(rtbuf,"%.12lf",(double)(*(double*)attachPtr[i].preptr));
			return(i);
		}
     		if(attachPtr[i].format == CF_CHAR){
	    	        sprintf(rtbuf,"%s",(char*)(attachPtr[i].preptr));
		}
                return(i);
	}
	if(strcmp(attachPtr[i].starsname,buf)==0){
     		if(attachPtr[i].format == CF_DOUBLE){
  	 	        sprintf(rtbuf,"%.12lf",(double)(*(double*)attachPtr[i].preptr));
			return(i);
		}
     		if(attachPtr[i].format == CF_CHAR){
	    	        sprintf(rtbuf,"%s",(char*)(attachPtr[i].preptr));
		}
                return(i);
	}
     }
     return(-1);	
}
void showsine(int id,int cc)
{
	int i;
	char frombuf[256];
	char rtbuf[256];

//     printf("mycc id:%d %d\n",id,cc);
     if (cc){
       printf("link %d : %s\n>",id,gLastStatusString); return;
     }
     for (i=0; i<ATTACH_NUM; i++) {
   		callbackstart = clock();
     	if(id == attachPtr[i].id){
     		if(attachPtr[i].format == CF_DOUBLE){
     			if((double)(*(double*)attachPtr[i].ptr) != (double)(*(double*)attachPtr[i].preptr)){
					(*(double*)attachPtr[i].preptr) = (double)(*(double*)attachPtr[i].ptr);
//			 	    printf("Changed Value=>");
//			 	    printf("%s %.12lf",attachPtr[i].name, (double)(*(double*)attachPtr[i].ptr));
			 	    sprintf(rtbuf,"%.12lf",(double)(*(double*)attachPtr[i].ptr));
			 	    sprintf(frombuf,"%s%s%s",MYNAME,".",attachPtr[i].name);

					starseventhandler(frombuf,"System","_ChangedValue",rtbuf);
					if(strcmp(attachPtr[i].name,attachPtr[i].starsname) != 0){
						starseventhandler(attachPtr[i].starsname,"System","_ChangedValue",rtbuf);
					}
     			}
		 	}
     		if(attachPtr[i].format == CF_CHAR){
     			if(strcmp((char*)(attachPtr[i].ptr),(char*)(attachPtr[i].preptr))!=0){
     				strcpy((char*)(attachPtr[i].preptr),(char*)(attachPtr[i].ptr));
//			 	    printf("Changed Value=>");
//			 	    printf("%s %s",attachPtr[i].name, attachPtr[i].ptr);
			 	    sprintf(frombuf,"%s%s%s",MYNAME,".",attachPtr[i].name);
			 	    sprintf(rtbuf,"%s",(char*)(attachPtr[i].ptr));
					starseventhandler(frombuf,"System","_ChangedValue",rtbuf);
					if(strcmp(attachPtr[i].name,attachPtr[i].starsname) != 0){
						starseventhandler(attachPtr[i].starsname,"System","_ChangedValue",rtbuf);
					}
     			}
		 	}
		 	
     	}
     }
//     printf("\n>");
}
void PostSystemInit(void)
{
  int i;
  int cc;  
  char devname[64], errstr[128];
  DTYPE dout;
  int sineID=-1;

  for(i=0;i<DOUBLE_NUM;i++)	pre_array_double[i]=-99999999999.0;
  for(i=0;i<CHAR_NUM;i++)	*pre_array_char[i]=(char)NULL;

  /* Establish DOUBLE : asyncrhonous call */
  sprintf(devname,"%s/device_0",DEVSRVNAME);
  for(i=0;i<ATTACH_NUM;i++){
	dout.dFormat = attachPtr[i].format;
	dout.dArrayLength = attachPtr[i].size;
	dout.data.vptr = attachPtr[i].ptr;
	sineID = AttachLink(devname,attachPtr[i].name, &dout, NULL, CA_READ, 100, showsine, CM_POLL|CM_BCAST);
  	if (sineID < 0){
	  printf("ATTACH ERROR: %s %d %s\n>", attachPtr[i].name,sineID,GetLastLinkError(-sineID,errstr));
#ifdef WINDOWS
	  exit(255);
#else
	  exit(0);
#endif
    }
	printf("ATTACHED: %s %d\n>", attachPtr[i].name,dout.data.vptr);
    attachPtr[i].id = sineID;
  }
}
int main_sub(char *nodename, char *myaddr)
{
  int cc;
  tineDebug=0;
  if(strcmp(myaddr,"")!=0){
	  printf("MYADDRESS: %s\n>", myaddr);
 
//	  strcpy(gtEthrAddr,gtEthrAddr);
	  SetGCastAddr(myaddr);
	  SetMCastAddr(myaddr);
	  printf("myip=%ld",getmyipaddr());
  }

  set_starsnodename(nodename);

  PostSystemInit();    /* call specific initialization: */

/*
  for(;;)
  {
    SystemCycle(TRUE);
  }
*/
  return 0;
}
