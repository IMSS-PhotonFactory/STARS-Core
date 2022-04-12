/*
* STARS interface library
* Takashi Kosuge (programming started on 2002-11-26)
* $Revision: 1.1 $
* $Date: 2010-01-19 02:56:39 $
*/

#define STARS_SVRN_MAX         128	
                 /*Maximum length+1 of stars server host name*/
#define STARS_DEFAULTPORT     6057
#define STARS_KFNAME_MAX       256
                 /*Maximum length+1 of keyfile name*/
#define STARS_MESSAGE_MAX   100000    /*STARS maximum message size*/
#define STARS_SETTIMEOUTMAX  30000
#define STARS_SETTIMEOUTMIN      1
#define STARS_CNTIMEOUT          5    /*timeout of connection*/
#define STARS_DEFAULTTIMEOUT     1    /*Read default timeout*/
#define STARS_BUF_KEY_READ     128    /*Buffer size for keyword*/
#define STARS_CALLBACK_MAX      32    /*Maximum callback point of mainloop function*/

typedef enum {
	STARS_CBMODE_STARS,
	STARS_CBMODE_CR,
	STARS_CBMODE_LF,
	STARS_CBMODE_DIRECT,
	STARS_CBMODE_DETECT
} STARS_CBMODE;

typedef struct {
	int    handle;                     /*socket port of stars connection*/
	struct timeval *timeout;           /*timeout of receive function*/
	char   rcvto[STARS_SVRN_MAX];	   /*Destination terminal name of receive function*/
                                       /*      normally, it will be this terminal name*/
	char   rcvfrom[STARS_SVRN_MAX];    /*Sender terminal name of receive function*/
	char   rcvmess[STARS_MESSAGE_MAX]; /*Received message*/
	int    rcvcnt;                /*Buffered postion which is used by callback routine*/
	STARS_CBMODE  cbmode;		  /*Callback mode*/
	int    (*cbfunc)();               /*Pointer of function which will be called*/
} STARS_CONNECTION;

