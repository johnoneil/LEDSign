



signon: signon.cpp JetfileII.hpp JetfileII.cpp
	g++ signon.cpp -lboost_system -lboost_thread -lpthread -o signon

signoff: signon.cpp JetfileII.hpp JetfileII.cpp
	g++ signoff.cpp -lboost_system -lboost_thread -lpthread -o signoff

emergencymsg: emergencymsg.cpp JetfileII.hpp JetfileII.cpp
	g++ emergencymsg.cpp -lboost_system -lboost_thread -lpthread -o emergencymsg

testcommand: testcommand.cpp JetfileII.hpp JetfileII.cpp
	g++ testcommand.cpp -lboost_system -lboost_thread -lpthread -o testcommand

all: signon signoff emergencymsg testcommand

clean:
	rm signon signoff emergencymsg
