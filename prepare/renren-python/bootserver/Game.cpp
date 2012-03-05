#include "Game.hpp"

Game::Game(void)
{
}

Game::~Game(void)
{
}

PyObject * Game::_instance = NULL;
char * Game::default_name = "server";

PyObject *Game::import(const char *name) {

	if (Game::_instance) {
		return _instance;
	}
	if (name == NULL) 
		name = Game::default_name;

	std::cout<<Game::default_name<<std::endl;

	_instance = PyImport_ImportModule(name);
	if (_instance == NULL) {
		std::cout<<"py import Game Failed"<<endl;

	}
	PyErr_Print();
	return _instance;
}

PyObject *Game::instance() {
	return Game::_instance;
}

void Game::run(int argc, char *args[]) {
	std::cout<<argc;
	PyObject *game = Game::instance();
	PyObject *game_dict = PyModule_GetDict(game);
	PyObject *run = PyDict_GetItemString(game_dict, "run");
	if (run == NULL) {

	}
	else {
		
		/*signal part */
		GameSignal *gs = new GameSignal();
		gs->registerSignal(SIGINT, signal_term);


		/* end signal part */

		PyObject *fun_args = PyTuple_New(argc);
		PyObject *run_args = PyTuple_New(1);
		for (int i = 0; i < argc; i++) {
			PyTuple_SetItem(fun_args, i, Py_BuildValue("s", args[i]));
		}

		PyTuple_SetItem(run_args, 0, fun_args);
		//PyTuple_SetItem(run_args, 1, Py_BuildValue("s", ","));
		PyObject *ret = PyObject_CallObject(run, run_args);

		if (ret == NULL) {
			PyErr_Print();
		}
	}
}

void Game::gameShutdown(int result){
	PyObject *game = Game::instance();
	PyObject *game_dict = PyModule_GetDict(game);
	PyObject *run = PyDict_GetItemString(game_dict, "onServerShutdown");
	PyObject_CallObject(run, NULL);

}


