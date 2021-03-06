/* vim: set ts=2 expandtab: */

/*
	file: JetfileII.hpp
	Author: John O'Neil
	Desc: JetfileII protocol implementation for controlling
	chainzone brand LED signs.
	This is the "2nd" (extended) protocol which isn't amenable
	to implementation in python due to large amounts of direct
	binary manipulation.
	
	Only partially implementing due to the fact I only need the
	following commands:
	1. Turn Sign On/Off
	2. Get sign on/off status
	3. Show emergency message for X seconds
	4. Manipulate playlist (my sign doesn't seem to handle the simplified
	protocol playlist manipulation)

*/
#include <string>
#include <sstream>
#include <algorithm>
#include <iostream>

typedef  unsigned long INT32U;
typedef  unsigned short INT16U;
typedef  unsigned char INT8U;
//*****************************************************************************
INT32U MsgCountCheckSumTwo(INT8U *buf, INT32U begin, INT32U end)
{
  INT32U i, check_sum;
  check_sum = 0;
  if (end >= begin)
  {
    i = end - begin;
    buf += begin;
    while(i--)
    {
      check_sum += *buf++;
    }
  }
  return check_sum;
}

//*********************************************************************
//**** Standard CRC-CCITT. x^0 + x^5 + x^12.
//*********************************************************************
INT16U const crc_ccitt_table[256] =
{
0x0000, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf,
0x8c48, 0x9dc1, 0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7,
0x1081, 0x0108, 0x3393, 0x221a, 0x56a5, 0x472c, 0x75b7, 0x643e,
0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64, 0xf9ff, 0xe876,
0x2102, 0x308b, 0x0210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5,
0x3183, 0x200a, 0x1291, 0x0318, 0x77a7, 0x662e, 0x54b5, 0x453c,
0xbdcb, 0xac42, 0x9ed9, 0x8f50, 0xfbef, 0xea66, 0xd8fd, 0xc974,
0x4204, 0x538d, 0x6116, 0x709f, 0x0420, 0x15a9, 0x2732, 0x36bb,
0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x0528, 0x37b3, 0x263a,
0xdecd, 0xcf44, 0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72,
0x6306, 0x728f, 0x4014, 0x519d, 0x2522, 0x34ab, 0x0630, 0x17b9,
0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3, 0x8a78, 0x9bf1,
0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x0738,
0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70,
0x8408, 0x9581, 0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7,
0x0840, 0x19c9, 0x2b52, 0x3adb, 0x4e64, 0x5fed, 0x6d76, 0x7cff,
0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324, 0xf1bf, 0xe036,
0x18c1, 0x0948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5,
0x2942, 0x38cb, 0x0a50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd,
0xb58b, 0xa402, 0x9699, 0x8710, 0xf3af, 0xe226, 0xd0bd, 0xc134,
0x39c3, 0x284a, 0x1ad1, 0x0b58, 0x7fe7, 0x6e6e, 0x5cf5, 0x4d7c,
0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
0x4a44, 0x5bcd, 0x6956, 0x78df, 0x0c60, 0x1de9, 0x2f72, 0x3efb,
0xd68d, 0xc704, 0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232,
0x5ac5, 0x4b4c, 0x79d7, 0x685e, 0x1ce1, 0x0d68, 0x3ff3, 0x2e7a,
0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3, 0x8238, 0x93b1,
0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0x0e70, 0x1ff9,
0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330,
0x7bc7, 0x6a4e, 0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0x0f78
};
//**********************************************************************
//**** FUNC: crc_ccitt_byte
//**** DESC: CRC 1 BYTE
//**** ARGS:
//**** crc - CRC VALUE
//**** c - char
//**** RETU:
//****

//***********************************************************************
__inline INT16U crc_ccitt_byte(INT16U crc, INT8U c)
{
  return (crc >> 8) ^ (INT16U)crc_ccitt_table[(crc ^ c) & 0xff];
}

namespace Jetfile2
{

namespace Text
{
  static const char Header[] = "QZ00SAX";
  static const char Coda = 0x4;
  static const char NewFrame = 0x0c;
  static const char NewLine = 0x0d;
  static const char Halfspace = 0x82;
namespace Flash
{
	static const char On[] = {0x07,'1'};
	static const char Off[] = {0x07,'0'};
}
namespace AutoTypeset
{
	static const char On[] = {0x1b,0x0a};
	static const char Off[] = {0x1b,0x0b};
}
namespace Background
{
	static const char Red[] = {0x1d,'0'};
	static const char Green[] = {0x1d,'1'};
	static const char Amber[] = {0x1d,'2'};
}

std::string Generate(const std::string& msg)
{
	std::string m = msg;
	//TODO: Process m for markup and turn into correct binary format.
	return Text::Header + msg + Text::Coda;
}

std::string Generate(const char* msg)
{
	return Text::Generate(std::string(msg));
}

//namespace Align
//{
//	static const char On[] = {0x1b,0x0a};
//	static const char Off[] = {0x1b,0x0b};
//}
/*  class AutoTypeset:
  Off = '\x1b0a'
  On = '\x1b0b'
class Background:
  Black = '\x1d0'
  Red = '\x1d1'
  Green = '\x1d2'
  Amber = '\x1d3'
class Align:
  class Vertical:
    Center = '\x1f0'
    Top = '\x1f1'
    Bottom = '\x1f2'
  class Horizontal:
    Center = '\x1e0'
    Left = '\x1e1'
    Right = '\x1e2' 
};*/

}//namespace Text

namespace Message
{
std::string INT16U2String(const INT16U v)
{
	std::string r;
	r += char( v & 0x00ff);
	r += char( (v & 0xff00) >> 8);
	return r;
};

std::string INT32U2String(const INT32U v)
{
	std::string r;
	r += char( v & 0x000000ff);
	r += char((v & 0x0000ff00) >> 8);
  r += char((v & 0x00ff0000) >> 16);
  r += char((v & 0xff000000) >> 24);
	return r;
}

std::string Checksum(const std::string& payload)
{
	const INT32U checksum32 = MsgCountCheckSumTwo(reinterpret_cast<INT8U*>(const_cast<char*>(payload.c_str())),0,payload.size());
	const INT16U checksum16 = static_cast< INT16U >(checksum32);
	return INT16U2String(checksum16);
}

std::string SYN(void)
{
	return INT16U2String(0xa755);
}
std::string EmergencyMessage(const char* msg, const INT16U t = 10)
{
	std::string m = Text::Generate(msg);
	const INT16U dataLen = m.size();
	//build the message backwards from the payload (data) to facilitate 
  //calculating the checksum.
	m = INT16U2String(t) + char(0x0) + char(0x0) + m;//time, sound, reserved
	m = char(0x0) + m;//flag
	m = char(0x1) + m;//arglength (arg is 1x4 bytes long)
	m = char(0x9) + m;//subcommand
	m = char(0x2) + m;//main command
	m = INT16U2String(0xabcd) + m;//packet serial
	m = char(0x0) + m;//source, dest addresses.
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = INT16U2String(dataLen) + m;
	m = Message::Checksum(m) + m;
	m = Message::SYN() + m;
	
	return m;
}

std::string TurnSignOn(void)
{
  std::string m;
	const INT16U dataLen = 0;
	//build the message backwards from the payload (data) to facilitate 
  //calculating the checksum.
	m = char(0x0) + m;//flag
	m = char(0x0) + m;//arglength (arg is 0 bytes long)
	m = char(0x4) + m;//subcommand
	m = char(0x4) + m;//main command
	m = INT16U2String(0xabcd) + m;//packet serial
	m = char(0x0) + m;//source, dest addresses.
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = INT16U2String(dataLen) + m;
	m = Message::Checksum(m) + m;
	m = Message::SYN() + m;
	
	return m;
}

std::string TurnSignOff(const bool sayGoodbye = false)
{
  std::string m;
	const INT16U dataLen = 0;
	//build the message backwards from the payload (data) to facilitate 
  //calculating the checksum.
  if(sayGoodbye)
  {
    m = INT32U2String(0) + m;
  }else{
    m = INT32U2String(1) + m;
  }
	m = char(0x0) + m;//flag
	m = char(0x1) + m;//arglength (arg is 1x4 bytes long)
	m = char(0x3) + m;//subcommand
	m = char(0x4) + m;//main command
	m = INT16U2String(0xabcd) + m;//packet serial
	m = char(0x0) + m;//source, dest addresses.
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = INT16U2String(dataLen) + m;
	m = Message::Checksum(m) + m;
	m = Message::SYN() + m;
	
	return m;
}

std::string TestCommand(void)
{
  std::string m;
	const INT16U dataLen = 0;
	//build the message backwards from the payload (data) to facilitate 
  //calculating the checksum.
	m = char(0x1) + m;//flag
	m = char(0x0) + m;//arglength (arg is 1x4 bytes long)
	m = char(0x1) + m;//subcommand
	m = char(0x3) + m;//main command
	m = INT16U2String(0xabcd) + m;//packet serial
	m = char(0x0) + m;//source, dest addresses.
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = char(0x0) + m;
	m = INT16U2String(dataLen) + m;
	m = Message::Checksum(m) + m;
	m = Message::SYN() + m;
	
	return m;
}





}//namespace Message

}//namespace jetfile2
