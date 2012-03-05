#pragma once
#include "Python.h"
#include <string>
#ifdef _WIN32
	#include <direct.h>
#else
	#include <unistd.h>
#endif

#include <vector>
#include <iostream>

namespace PyInit {
	extern  const std::string root_dir;
	extern std::string sys_paths;
	extern std::vector<std::string> python_paths;
	void init();
	void appendSysPaths();
	void appendSysPath(const char *path);
	char *work_dir(char *buf, int maxLen);
};