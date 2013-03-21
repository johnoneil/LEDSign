
#include <iostream>
using std::cout;
using std::endl;

#include <boost/asio.hpp>
using namespace::boost::asio;

#include "JetfileII.hpp"


void dump(unsigned char * buffer, size_t size)
{
	//cout.setf(ios::hex,ios::basefield);
	for(size_t sz = 0; sz < size; ++sz)
	{
		cout<<std::hex<<static_cast<int>(buffer[sz])<<"__";
	}
	cout<<endl;
};
 

int main(int argc, char* argv[])
{
	Jetfile2::EmergencyMsg msg(Jetfile2::Text::Generate("Hello there. How are you?"));
	cout<<"The size of msg is " << msg.Size() <<endl;
	cout<<"checksum of msg is " << msg.header.Checksum<<endl;

	//newer version to construct message
	std::string message2 = Jetfile2::Message::EmergencyMessage("Hello there. How are you?");
	cout<<"The size of msg2 is " << message2.size() <<endl;

	serial_port_base::baud_rate BAUD(19200);
	serial_port_base::parity PARITY(serial_port_base::parity::none);
	serial_port_base::stop_bits STOP(serial_port_base::stop_bits::one);
	io_service io;
        serial_port port(io, "/dev/ttyS0");

        port.set_option(BAUD);
        port.set_option(PARITY);
        port.set_option(STOP);
	
	dump(reinterpret_cast<unsigned char*>(&msg),msg.Size());
	cout<<"msg 2 is:"<<endl;
	dump(reinterpret_cast<unsigned char*>(const_cast<char*>(message2.c_str())),message2.size());

        //write(port, buffer(&msg,msg.Size()));
	write(port,buffer(message2,message2.size()));
	
	return 0;
}
