/*
* STARS interface library
* Origin 2002-11-26
* Takashi Kosuge
* $Revision: 1.1 $
* $Date: 2010-01-19 02:56:39 $
*/

/*WINDOWS, WINDLL(requires define WINDOWS), OS9, LINUX*/

#include <stdio.h>
#include <string.h>
#include <sys/types.h>     /* socket() */
#include <stdlib.h>        /* atol */

#ifdef WINDOWS
#  include <winsock.h>
#  include <io.h>
#  define bcopy(a,b,c) memcpy(b,a,c)
#endif

#ifdef OS9
#  include <sys/socket.h>    /* socket() */
#  include <netinet/in.h>    /* struct sockaddr_in */
#  include <netdb.h>         /* gethostbyname() */
#  include <UNIX/os9def.h>   /* socket */
#  include <modes.h>         /* socket */
#  include <UNIX/os9types.h> /* select */
#  include <types.h>         /* select */
#endif

#ifdef LINUX
#  include <sys/socket.h>
#  include <netdb.h>         /* gethostbyname() */
#endif


#include "starsif.h"
#include "starsfnc.h"
#define STARS_TRUE             1
#define STARS_FALSE            0


int _stars_get_keyword(char *keyfile, char *keybuf, long keynumber);
int _stars_tcp_connect(char *hostname, int portno);
int _stars_send_direct(int sockn, char *message);
int _stars_receive_lf(int sockn, char *message, struct timeval *timeout, int buflen);
int _stars_strltrim(char *p1, char *p2);
void _stars_divide_message(STARS_CONNECTION *scp);


STARS_CONNECTION *stars_callback_list[STARS_CALLBACK_MAX];
int stars_callback_list_count = 0;

STARS_CONNECTION *stars_alloc(){
	STARS_CONNECTION *scp;
	struct timeval *timeout;
	scp = (STARS_CONNECTION *) malloc(sizeof *scp);
	timeout = (struct timeval *) malloc(sizeof *timeout);
	scp->rcvfrom[0] = (char)0;
	scp->rcvto[0]   = (char)0;
	scp->rcvmess[0] = (char)0;
	scp->rcvcnt     = 0;
	scp->timeout    = timeout;
	scp->cbmode     = STARS_CBMODE_STARS;
	scp->cbfunc     = NULL;
	stars_set_timeout(scp, STARS_DEFAULTTIMEOUT);
	return(scp);
}
/*Create structure of STARS connection*/
STARS_CONNECTION *stars_open(char *nodename, char *svrhost, int svrport, char *keyfile){
	STARS_CONNECTION *scp;

	char keybuf[STARS_BUF_KEY_READ];
	char msgbuf[STARS_MESSAGE_MAX];
	int  sockn;
	long keynumber;
	struct timeval cntimeout;
#   ifdef WINDOWS
	static WSADATA wsaData;
	static int wsaInitialized = 0;

	if (!wsaInitialized)
	{
		wsaInitialized = -1;
		WSAStartup(0x0101,&wsaData);
	}
#   endif

	cntimeout.tv_sec  = STARS_CNTIMEOUT;
	cntimeout.tv_usec = 0L;

/*Open socket*/
	if((sockn = _stars_tcp_connect(svrhost, svrport)) < 0){return(NULL);}

/*Receive key number*/
	if(_stars_receive_lf(sockn, keybuf, &cntimeout, STARS_BUF_KEY_READ) < 1){
		close(sockn);
		return(NULL);
	}
	keynumber = atol(keybuf);

/*Get keyword*/
	if(_stars_get_keyword(keyfile, keybuf, keynumber) != STARS_TRUE){
		close(sockn);
		return(NULL);
	}

/*Send keyword*/
	strcpy(msgbuf, nodename);
	strcat(msgbuf, " ");
	strcat(msgbuf, keybuf);
	if(_stars_send_direct(sockn, msgbuf) < 0){
		close(sockn);
		return(NULL);
	}

/*Wait for Ok:*/
	if(_stars_receive_lf(sockn, msgbuf, &cntimeout, STARS_MESSAGE_MAX) < 1){
		close(sockn);
		return(NULL);
	}

/*Create structure of STARS connection*/
	scp = stars_alloc();
	scp->handle   = sockn;
	return(scp);
}

/*Send messge to stars server (internal)*/
int _stars_send_direct(int sockn, char *message){
	int buflen;
	char buf[STARS_MESSAGE_MAX+1];
	strcpy(buf, message);
	buflen = strlen(buf);
	buf[buflen] = (char)0x0a;
	buflen++; 
	return(send(sockn, buf, buflen, 0));
}

/*Receive message with LF (internal)*/
int _stars_receive_lf(int sockn, char *message, struct timeval *timeout, int buflen){
	int rt;
	int rdp;
	char buf[2];
	fd_set readfds,readfds_save;

	rdp = 0;
	while(1){
		FD_ZERO(&readfds_save);
		FD_SET(sockn, &readfds_save);
		readfds = readfds_save;
		rt=select(FD_SETSIZE, &readfds, NULL, NULL, timeout);
		if(rt <= 0){
			return(rt);
		}else{
			recv(sockn, buf, 1, 0);
			if(buf[0] == (char)0x0a){
				 message[rdp] = (char)0;
				 return(rdp);
			}
			message[rdp] = buf[0];
			if(rdp < buflen){
				rdp++;
			}
		}
	}
}

/*Make TCP/IP connection (internal)*/
int _stars_tcp_connect(char *hostname, int portno){
	struct hostent *hostent;
	struct sockaddr_in addr;
/*	int addr_len;*/
	int sn ;
		addr.sin_family = AF_INET ;
		if((hostent = gethostbyname( hostname )) == NULL){
			return(-1);
		}
		bcopy(hostent->h_addr, &addr.sin_addr, hostent->h_length);
		addr.sin_port = htons( (unsigned short)portno );
		if((sn = socket(AF_INET, SOCK_STREAM, 0)) < 0){
			return(-1);
        }
		if( connect(sn, (struct sockaddr *)&addr, sizeof(addr)) < 0 ){
			close(sn);
			return(-1);
        }
		return(sn);
}

/*Get keyword from key file (internal)*/
int _stars_get_keyword(char *keyfile, char *keybuf, long keynumber){
	FILE *keyfp;
	long keycount=0;
	long keyfind;

	if((keyfp = fopen(keyfile, "r")) == NULL){
		return(STARS_FALSE);
	}
	while(!feof(keyfp)){
		if(fscanf(keyfp, "%s", keybuf) != 1){break;}
		keycount++;
	}
	rewind(keyfp);
	keyfind = keynumber % keycount;
	for(keycount = 0; keycount <= keyfind; keycount++){
		if(fscanf(keyfp, "%s", keybuf) != 1){break;}
	}
	fclose(keyfp);
	return(STARS_TRUE);	
}

/*Release structure of STARS connection*/
void  stars_free(STARS_CONNECTION *scp){
	free(scp->timeout);
	free(scp);
}

/*Close STARS connection*/
int stars_close(STARS_CONNECTION *scp){
	//_stars_send_direct(scp->handle, "quit");
	close(scp->handle);
	stars_free(scp);
	return(1);
}

/*Set timeout for receiving message from STARS server*/
void  stars_set_timeout(STARS_CONNECTION *scp, int timeout){
	if(timeout > STARS_SETTIMEOUTMAX){return;}
	if(timeout < STARS_SETTIMEOUTMIN){return;}
	scp->timeout->tv_sec  = ((long)timeout)/1000L;
	scp->timeout->tv_usec = (((long)timeout) - (scp->timeout->tv_sec * 1000L)) * 1000L;
}

/*Get timeout for receiving message from STARS server*/
int stars_get_timeout(STARS_CONNECTION *scp){
	return( (int)((scp->timeout->tv_sec * 1000L) + (scp->timeout->tv_usec / 1000L)) );
}

/*Get socket number of STARS connection*/
int   stars_get_handle(STARS_CONNECTION *scp){
	return(scp->handle);
}

int stars_send(STARS_CONNECTION *scp, char *message, char *sendto){
	int buflen;
	char buf[STARS_MESSAGE_MAX+1];
	buf[0] = (char) 0;
	if(sendto != NULL){
		strcpy(buf, sendto);
		strcat(buf, " ");
	}
	strcat(buf, message);
	buflen = strlen(buf);
	buf[buflen] = (char)0x0a;
	buflen++; 
	return(send(scp->handle, buf, buflen, 0));
}

int   stars_receive(STARS_CONNECTION *scp){
	int rt;

	rt = _stars_receive_lf(scp->handle, scp->rcvmess, scp->timeout, STARS_MESSAGE_MAX);
	if(rt <= 0){return(rt);}
	_stars_divide_message(scp);

	return(rt);
}	

void _stars_divide_message(STARS_CONNECTION *scp){
	char *pos;

	if((pos=strchr(scp->rcvmess, '>')) == NULL){return;}
	pos[0]=(char)0;
	strcpy(scp->rcvfrom, scp->rcvmess);
	_stars_strltrim(scp->rcvmess, ++pos);
	if((pos=strchr(scp->rcvmess, ' ')) == NULL){return;}
	pos[0]=(char)0;
	strcpy(scp->rcvto, scp->rcvmess);
	_stars_strltrim(scp->rcvmess, ++pos);
}

int _stars_strltrim(char *p1, char *p2){
	while(*p2 != (char)0){
		*p1 = *p2;
		p1++;
		p2++;
	}
	*p1 = (char) 0;
	return 0;
}

int stars_act(STARS_CONNECTION *scp, char *message){
	int rt;
	if((rt = stars_send(scp, message, NULL)) < 0){
		return(rt);
	}
	return(stars_receive(scp));
}

int stars_add_callback(STARS_CONNECTION *scp){
	if(scp->cbfunc == NULL){return(-1);}
	stars_callback_list[stars_callback_list_count] = scp;
	stars_callback_list_count++;
	return(stars_callback_list_count);
}

int stars_mainloop(int timeout){
	return 1;
}	

#ifdef WINDLL
__declspec(dllexport) void PASCAL StarsFree(STARS_CONNECTION *scp){
	stars_free(scp);
}

/*Close STARS connection*/
__declspec(dllexport) short PASCAL StarsClose(STARS_CONNECTION *scp){
	return stars_close(scp);
}

/*Set timeout for receiving message from STARS server*/
__declspec(dllexport) void PASCAL  StarsSetTimeout(STARS_CONNECTION *scp, int timeout)
{
	stars_set_timeout(scp,timeout);
}
__declspec(dllexport) short PASCAL StarsOpen(char *nodename, char *svrhost, int svrport, char *keyfile, STARS_CONNECTION *sc)
{
	STARS_CONNECTION *scp = NULL;
    scp = stars_open(nodename,svrhost,svrport,keyfile);
	if (scp != NULL) memcpy(sc,scp,sizeof(STARS_CONNECTION));
    return scp != NULL ? 0 : -1;
} 
__declspec(dllexport) short PASCAL StarsSend(STARS_CONNECTION *scp, char *message, char *sendto){
  return stars_send(scp,message,sendto);
}
__declspec(dllexport) short PASCAL StarsReceive(STARS_CONNECTION *scp){
  return stars_receive(scp);
}
__declspec(dllexport) short PASCAL StarsAddCallback(STARS_CONNECTION *scp){
	return stars_add_callback(scp);
}
__declspec(dllexport) short PASCAL StarsAct(STARS_CONNECTION *scp, char *message){
	return stars_act(scp,message);
}
__declspec(dllexport) short PASCAL StarsGetTimeout(STARS_CONNECTION *scp){
	return stars_get_timeout(scp);
}
__declspec(dllexport) short PASCAL StarsGetHandle(STARS_CONNECTION *scp){
	return stars_get_handle(scp);
}
char lpszStarsWnd[] = "STARS DLL Window";
HANDLE hStarsWnd = 0;
__declspec(dllexport) LRESULT CALLBACK StarsWndProc(HWND hWnd, WORD iMessage, WORD wParam, LONG lParam)
{
  switch (iMessage)
  {
    case WM_TIMER:
      stars_mainloop(10);
      break;
    case WM_DESTROY:
      KillTimer(hWnd,1);
    default:
      return DefWindowProc (hWnd, iMessage, wParam, lParam);
  }
  return 0;
}
int RegisterStarsWindow(HANDLE hInst)
{
	static WNDCLASS wndclass;

	wndclass.style         = CS_GLOBALCLASS|CS_SAVEBITS;  /* essential style!! */
	wndclass.lpfnWndProc   = (WNDPROC) StarsWndProc;
	wndclass.cbClsExtra    = 0;
	wndclass.cbWndExtra    = 0;
	wndclass.hInstance     = hInst;
	wndclass.hIcon         = LoadIcon (0, IDI_APPLICATION);
	wndclass.hCursor       = LoadCursor (0, IDC_ARROW);
	wndclass.hbrBackground = GetStockObject (WHITE_BRUSH);
	wndclass.lpszMenuName  = 0;
	wndclass.lpszClassName = lpszStarsWnd;

	if (!RegisterClass(&wndclass)) return -1;
	return 0;
}
int CreateStarsWindow(HANDLE hInst)
{
	if (RegisterStarsWindow(hInst)) return -1;
	if (!(hStarsWnd = CreateWindow (
							lpszStarsWnd, lpszStarsWnd,   /* lpClassName, lpWindowName */
							WS_BORDER|WS_CAPTION,         /* dwStyle                   */
							CW_USEDEFAULT, CW_USEDEFAULT, /* X, Y                      */
							CW_USEDEFAULT, CW_USEDEFAULT, /* nWidth, nHeight           */
							0, 0,                         /* hWndParent, hMenu         */
							hInst,                        /* hInstance                 */
							NULL                          /* createstruct              */
		 ) ) ) return -1;

	SetTimer(hStarsWnd,1,100,(FARPROC)NULL);
	return 0;
}
BOOL WINAPI DllMain(HINSTANCE hInstDll,DWORD fdwReason,LPVOID lpvReserved)
{
  switch (fdwReason)
  {
    case DLL_PROCESS_ATTACH:  // DLL being loaded
	  CreateStarsWindow(hInstDll);
//      stars_mainloop(STARS_DEFAULTTIMEOUT);
	  break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
    case DLL_PROCESS_DETACH:  // DLL being unloaded
      break;
  }
  return (TRUE);
}

#endif
