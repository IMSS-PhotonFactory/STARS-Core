/*
* STARS interface library (Functions)
* Takashi Kosuge (programming started on 2002-11-26)
* $Revision: 1.1 $
* $Date: 2010-01-19 02:56:39 $
*/


extern STARS_CONNECTION *stars_alloc();
extern STARS_CONNECTION *stars_open(char *nodename, char *svrhost, int svrport, char *keyfile);
extern void  stars_free(STARS_CONNECTION *scp);
extern int   stars_close(STARS_CONNECTION *scp);
extern void  stars_set_timeout(STARS_CONNECTION *scp, int timeout);
extern int   stars_get_timeout(STARS_CONNECTION *scp);
extern int   stars_get_handle(STARS_CONNECTION *scp);
extern int   stars_send(STARS_CONNECTION *scp, char *message, char *sendto);
extern int   stars_receive(STARS_CONNECTION *scp);
extern int   stars_add_callback(STARS_CONNECTION *scp);
extern int   stars_mainloop(int timeout);
