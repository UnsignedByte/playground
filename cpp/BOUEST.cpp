#include <iostream>
#include <fstream>
#include <cstring>
#include <algorithm>
#include <set>
#include <deque>
#include <vector>
#include <queue>
#include <stack>
#include <cmath>
#include <boost>

using namespace std;

#define INF 2147483647
#define LLINF 9223372036854775807
#define EPS 10e-9
#define HASHPRIME int(10e9+7)

boost::variant<int, double, string> egg(int a) {
	if (a==1)
		return "stringy";
	else if (a==3)
		return 1.5;
	else
		return 3;
}

int main(){
	cout << egg(1) << endl;
	cout << egg(0) << endl;
	cout << egg(3) << endl;
	return 0;
}