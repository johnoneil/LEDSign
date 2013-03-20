



signon: signon.cpp JetfileII.hpp JetfileII.cpp
	g++ signon.cpp -lboost_system -lboost_thread -lpthread -o signon

signoff: signon.cpp JetfileII.hpp JetfileII.cpp
	g++ signoff.cpp -lboost_system -lboost_thread -lpthread -o signoff

all: signon signoff

clean:
	rm signon signoff
