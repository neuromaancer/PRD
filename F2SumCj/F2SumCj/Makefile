
HOMEDIR=/docsrv/grosso
INCLUDE=-I$(HOMEDIR)/include -I.
CC=c++
#CFLAGS=-c -Wall -g $(INCLUDE)
CFLAGS=-c -Wall -O3 -DNDEBUG $(INCLUDE)
LIBS=-L$(HOMEDIR)/lib -lconcert -lilocplex -lcplex -lpthread 

f2ft:	f2ft.o
	$(CC) f2ft.o $(LIBS) -o f2ft
bound:	bound.o
	$(CC) bound.o $(LIBS) -o bound
.cpp.o:
	$(CC) $(CFLAGS) $< -o $@
.c.o:
	cc $(CFLAGS) $< -o $@
clean:
	rm *.o f2ft
