#include "common.hpp"

namespace PyInit {
	const std::string root_dir("F:\\opensource\\flash\\renren\\server");
	std::vector<std::string> python_paths;
	std::string sys_paths = "";
	
	void appendSysPaths() {
		char cur_dir[256];
		work_dir(cur_dir,256);
		//const std::string s(cur_dir);
		const std::string s("F:\\opensource\\flash\\renren\\server");
#ifdef _WIN32
		const char endchar = ';';
#else
		const char endchar = ':';
#endif
		python_paths.push_back(s);
		python_paths.push_back(s + "\\pylibs");
		python_paths.push_back(s + "\\pylibs\\Lib");
		python_paths.push_back(s + "\\pylibs\\DLLs");
		python_paths.push_back(s + "\\pylibs\\Lib\\site-packages");
		std::vector<std::string>::const_iterator pp = python_paths.begin();
		for(pp; pp!=python_paths.end(); pp++) {
			sys_paths += (*pp + endchar);
		}
		appendSysPath(sys_paths.c_str());

	}

	/*
	Set sys.path to a list object of paths found in path
	which should be a list of paths separated with the platform¡¯s search path delimiter 
	(: on Unix, ; on Windows).
	*/
	void appendSysPath(const char *p) {
		PySys_SetPath(const_cast<char*>(p));
	}

	void init() {Py_Initialize();};

	char *work_dir(char *buf, int maxLen){
#ifdef _WIN32
		return _getcwd(buf, maxLen);
#else
		return getcwd(buf, maxLen);
#endif
	}
};