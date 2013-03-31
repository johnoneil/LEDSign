/* vim: set ts=2 expandtab: */
#include <iostream>
#include <vector>
using std::cout;
using std::endl;

#include <boost/asio.hpp>
using namespace::boost::asio;
#include <boost/bind.hpp>

#include "JetfileII.hpp"


void dump(unsigned char * buffer, size_t size)
{
	for(size_t sz = 0; sz < size; ++sz)
	{
		cout<<std::hex<<static_cast<int>(buffer[sz])<<"__";
	}
	cout<<endl;
};
void handler(
  const boost::system::error_code& error, // Result of operation.

  std::size_t bytes_transferred           // Number of bytes copied into the
                                          // buffers. If an error occurred,
                                          // this will be the  number of
                                          // bytes successfully transferred
                                          // prior to the error.
)
{
  if(error)
  {
    cout<<"Error reading bytes :"<<error.message()<<endl;
  }
  cout<<"bytes transferred :" <<static_cast<int>(bytes_transferred)<< endl;
}

void read_callback(bool& data_available, deadline_timer& timeout, const boost::system::error_code& error, std::size_t bytes_transferred)
{
  cout<<"read_callback "<<bytes_transferred<<endl;
  if (error || !bytes_transferred)
  {
    // No data was read!
    data_available = false;
    return;
  }

  //timeout.cancel();  // will cause wait_callback to fire with an error
  data_available = true;
}

void wait_callback(serial_port& port, const boost::system::error_code& error)
{
  cout<<"wait callback fired."<<endl;
  if (error)
  {
    // Data was read and this timeout was canceled
    return;
  }

  port.cancel();  // will cause read_callback to fire with an error
}

void wh(const boost::system::error_code& ec,
        std::size_t bytes_transferred)
{
    std::cout << "test";
};

int main(int argc, char* argv[])
{
	//construct message
	//std::string message = Jetfile2::Message::EmergencyMessage("Hello there. How are you?");
  //std::string message = Jetfile2::Message::TurnSignOff();
  //std::string message = Jetfile2::Message::TurnSignOn(); 
  std::string message = Jetfile2::Message::TestCommand(); 
	cout<<"The size of msg is " << message.size() <<endl;

	serial_port_base::baud_rate BAUD(19200);
	serial_port_base::parity PARITY(serial_port_base::parity::none);
	serial_port_base::stop_bits STOP(serial_port_base::stop_bits::one);
	io_service io;
  serial_port port(io, "/dev/ttyS0");

  port.set_option(BAUD);
  port.set_option(PARITY);
  port.set_option(STOP);

  //set up serial port read with timeout
  deadline_timer timeout(io);
  bool data_available = false;
  std::size_t bytes_transferred = 0;
  std::vector<uint8_t> buf(1024);
  //port.async_write(buffer(message,message.size()));
  /*boost::asio::async_write(
        port,
        boost::asio::buffer(message,message.size()),
        boost::bind(
            &wh,
            boost::asio::placeholders::error,
            boost::asio::placeholders::bytes_transferred)
       );*/
  port.async_write_some(boost::asio::buffer(message,message.size()),&wh);
  /*port.async_read_some(boost::asio::buffer(buf),
        boost::bind(&read_callback, boost::ref(data_available), boost::ref(timeout),
                  boost::asio::placeholders::error,
                  //boost::ref(bytes_transferred)));*/
  async_read(port,boost::asio::buffer(buf,buf.size()),handler);
                  //boost::asio::placeholders::bytes_transferred));
  timeout.expires_from_now(boost::posix_time::milliseconds(10000));
  timeout.async_wait(boost::bind(&wait_callback, boost::ref(port),
                  boost::asio::placeholders::error));

  cout<<"msg is:"<<endl;
	dump(reinterpret_cast<unsigned char*>(const_cast<char*>(message.c_str())),message.size());

	//write(port,buffer(message,message.size()));

  io.run();  // will block until async callbacks are finished

  //cout<<"read "<<bytes_transferred<<" and data avail"<< data_available <<endl;

  //size_t len = read(port, boost::asio::buffer(buf));
  //dump(reinterpret_cast<unsigned char*>(const_cast<char*>(message.c_str())),message.size());
	
	return 0;
}
