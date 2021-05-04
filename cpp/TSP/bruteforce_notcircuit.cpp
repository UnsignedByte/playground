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

using namespace std;

#define INF 2147483647
#define LLINF 9223372036854775807
#define EPS 10e-9
#define HASHPRIME int(10e9+7)

size_t N;

struct path {
	int visited;
	int length;
	int id;
	string route;
	bool operator<(const path& rhs) const
  {
      return length < rhs.length;
  }
};
int main(){
	ifstream fin;
	fin.open("tsp.in");
	ofstream fout;
	fout.open("tsp.out");

	fin >> N;

	int graph[N][N];

	for (int i = 0; i < N; i++){
		for(int j = 0; j < N; j++) {
			fin >> graph[i][j];
		}
	}

	int min_length = INF;
	string min_route;
	queue<path> q;
	q.push((path){1,0,0,"0"});
	while(!q.empty()) {
		path p = q.front();
		q.pop();
		// cout << p.length << " " << p.visited << " " << p.id << endl;
		for(int i = 0; i < N; i++){
			if (i==0 && p.visited == (1<<N) -1 && p.id==7) {
				if (p.length<min_length) {
					// cout << p.route << endl;
					min_length = p.length;
					min_route = p.route;
				}
				continue;
			}
			if(!(p.visited & (1<<i))) {
				q.push((path){p.visited+(1<<i), p.length+graph[p.id][i], i, p.route+","+to_string(i)});
			}
		}
	}
	fout << min_length << endl;
	fout << min_route << endl;
	return 0;
}