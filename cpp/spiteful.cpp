/*
* @Author: UnsignedByte
* @Date:   2022-02-16 15:04:58
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2022-02-16 15:30:40
*/

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
#include <random>

#define INF 2147483647
#define LLINF 9223372036854775807
#define EPS 10e-9
#define HASHPRIME int(10e9+7)

const uint32_t trials = 10000000;

int main(){

	std::random_device engine;
  std::mt19937 rng(engine());
  std::uniform_real_distribution<double> urand(0., 1.); // distribution in range [1, 6]

	uint32_t total = 0;

	for (int i = 0; i < trials; i++) {
		int count = 4;
		int spite = 1;

		while (count > 0) {
			total++;
			if (urand(rng) * (spite + 2) < 2) {
				count--;
			} else {
				spite++;
			}
		}
	}

	printf("Turns taken: %d, Trials: %d\n", total, trials);

	return 0;
}