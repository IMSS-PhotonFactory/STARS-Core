
__declspec(dllimport) void PASCAL StarsFree(STARS_CONNECTION *scp);
__declspec(dllimport) short PASCAL StarsClose(STARS_CONNECTION *scp);
__declspec(dllimport) void PASCAL  StarsSetTimeout(STARS_CONNECTION *scp, int timeout);
__declspec(dllimport) short PASCAL StarsOpen(char *nodename, char *svrhost, int svrport, char *keyfile, STARS_CONNECTION *sc);
__declspec(dllimport) short PASCAL StarsSend(STARS_CONNECTION *scp, char *message, char *sendto);
__declspec(dllimport) short PASCAL StarsReceive(STARS_CONNECTION *scp);
__declspec(dllimport) short PASCAL StarsAddCallback(STARS_CONNECTION *scp);
__declspec(dllimport) short PASCAL StarsAct(STARS_CONNECTION *scp, char *message);
__declspec(dllimport) short PASCAL StarsGetTimeout(STARS_CONNECTION *scp);
__declspec(dllimport) short PASCAL StarsGetHandle(STARS_CONNECTION *scp);

