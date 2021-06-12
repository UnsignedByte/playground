/*
* @Author: almundmilk
* @Date:   2021-06-11 19:44:05
* @Last Modified by:   almundmilk
* @Last Modified time: 2021-06-11 19:45:01
*/

#include "first_app.hpp"

namespace lve {
	void FirstApp::run() {
		while(!lveWindow.shouldClose()) {
			glfwPollEvents();
		}
	}
}