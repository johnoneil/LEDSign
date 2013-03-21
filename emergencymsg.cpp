/* vim: set ts=2 expandtab: */
#include <iostream>
using std::cout;
using std::endl;

#include <boost/asio.hpp>
using namespace::boost::asio;

#include "JetfileII.hpp"


void dump(unsigned char * buffer, size_t size)
{
	for(size_t sz = 0; sz < size; ++sz)
	{
		cout<<std::hex<<static_cast<int>(buffer[sz])<<"__";
	}
	cout<<endl;
};
 

int main(int argc, char* argv[])
{
	//construct message
	std::string message = Jetfile2::Message::EmergencyMessage("Hello there. How are you?");
	cout<<"The size of msg is " << message.size() <<endl;

	serial_port_base::baud_rate BAUD(19200);
	serial_port_base::parity PARITY(serial_port_base::parity::none);
	serial_port_base::stop_bits STOP(serial_port_base::stop_bits::one);
	io_service io;
  serial_port port(io, "/dev/ttyS0");

  port.set_option(BAUD);
  port.set_option(PARITY);
  port.set_option(STOP);
	
	cout<<"msg is:"<<endl;
	dump(reinterpret_cast<unsigned char*>(const_cast<char*>(message.c_str())),message.size());

	write(port,buffer(message,message.size()));
	
	return 0;
}
