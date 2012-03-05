#pragma once
#include <signal.h>
#include <iostream>
#include "Game.hpp"
using namespace std;
void signal_term(int signal_num);

class GameSignal
{
public:
	GameSignal(void);
	~GameSignal(void);
	void registerSignal(int signal_num, void(*fun)(int));
};

