#pragma once
#include "Python.h"
class PythonAPI
{
public:
	PythonAPI(void);
	~PythonAPI(void);
	void py_init() { Py_Initialize();}


};

