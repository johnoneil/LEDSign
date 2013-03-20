



signon: signon.cpp JetfileII.hpp JetfileII.cpp
	g++ signon.cpp -lboost_system -lboost_thread -lpthread -o signon

signoff: signon.cpp JetfileII.hpp JetfileII.cpp
	g++ signoff.cpp -lboost_system -lboost_thread -lpthread -o signoff

emergencymsg: emergencymsg.cpp JetfileII.hpp JetfileII.cpp
	g++ emergencymsg.cpp -lboost_system -lboost_thread -lpthread -o emergencymsg

all: signon signoff emergencymsg

clean:
	rm signon signoff emergencymsg
