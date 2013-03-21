/* vim: set ts=2 expandtab: */
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
	//Jetfile2::SignOffMsg msg;
	//Jetfile2::SignOnMsg msg;
  std::string msg = Jetfile2::Message::TurnSignOff(true);
	cout<<"The size of msg is " << msg.size()<<endl;

	serial_port_base::baud_rate BAUD(19200);
	serial_port_base::parity PARITY(serial_port_base::parity::none);
	serial_port_base::stop_bits STOP(serial_port_base::stop_bits::one);
	io_service io;
  serial_port port(io, "/dev/ttyS0");

  port.set_option(BAUD);
  port.set_option(PARITY);
  port.set_option(STOP);
	
  cout<<"msg is:"<<endl;
	dump(reinterpret_cast<unsigned char*>(const_cast<char*>(msg.c_str())),msg.size());

	write(port,buffer(msg,msg.size()));
	
	return 0;
}
