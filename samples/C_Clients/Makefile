all: ucsample.o icsample.o starsif.o
	cc -o icsample icsample.o starsif.o
	cc -o ucsample ucsample.o starsif.o

icsample: icsample.o starsif.o
	cc -o icsample icsample.o starsif.o

ucsample: ucsample.o starsif.o
	cc -o ucsample ucsample.o starsif.o


icsample.o: icsample.c starsif.h starsfnc.h
	cc -c icsample.c -I./

ucsample.o: ucsample.c starsif.h starsfnc.h
	cc -c ucsample.c -I./

starsif.o: starsif.c starsif.h starsfnc.h
	cc -c starsif.c -I./

clean:
	rm -f ucsample
	rm -f icsample
	rm -f ucsample.o icsample.o starsif.o
