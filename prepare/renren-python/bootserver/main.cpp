#include <iostream>
#include "Game.hpp"
#include "common.hpp"

int main(int argc, char *args[]) {
	PyInit::init();
	PyInit::appendSysPaths();
	Game::import();
	Game::run(argc, args);
	getchar();

}
