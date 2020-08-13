#include <iostream>
#include <locale>
#include <codecvt>
#include <string>

#define INF 2147483647
#define LLINF 9223372036854775807
#define EPS 10e-9
#define HASHPRIME int(10e9+7)


int main(){
	std::basic_string<char16_t> inp("egg");
  std::wstring_convert<std::codecvt_utf8_utf16<char16_t>,char16_t> convert;
  std::string fnameStr = convert.to_bytes(inp);
  std::cout << inp << std::endl;
  std::cout << fnameStr << std::endl;

	return 0;
}