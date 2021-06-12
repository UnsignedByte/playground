/*
* @Author: almundmilk
* @Date:   2021-06-11 18:07:28
* @Last Modified by:   almundmilk
* @Last Modified time: 2021-06-11 19:43:18
*/

#include "first_app.hpp"

#include <cstdlib>
#include <iostream>
#include <stdexcept>

int main() {
	lve::FirstApp app{};

	try {
		app.run();
	} catch (const std::exception &e) {
		std::cerr << e.what() << '\n';
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}