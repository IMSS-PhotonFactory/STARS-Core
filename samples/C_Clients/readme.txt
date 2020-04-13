## Sample program STARS C clients ##

I checked this samples run on Linux (Fedra Core 4 /2.6.11-1.1369_FC4).
This sample has 2 types of program. "icsample.c" fits I/O client and "ucsample.c" fits
user client.

2006-02-08 Takashi Kosuge


1. Copy 3 files shown below from starsclib directory in STARS distribution package
   to this directory.

     starsfnc.h
     starsif.h
     starsif.c

2. Modify definition (#define LINUX) in the starsif.c.

:
/*WINDOWS, OS9, LINUX*/
#define LINUX
        ~~~~~

#include <stdio.h>
#include <string.h>
:

3. Enter make!

4. Copy "icsample.key" and "ucsample.key" into takaserv-lib.
