#pragma once
#include <iostream>
#include "Python.h"
#include "GameSignal.hpp"

class Game
{
	
public:
	~Game(void);
	static char *default_name;
	static PyObject *_instance;
	static PyObject *import(const char *name = NULL);
	static PyObject *instance();
	static void run(int argv, char *args[]);
	static void gameShutdown(int result);
private:
		Game(void);
};



