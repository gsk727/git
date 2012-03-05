#include "GameSignal.hpp"

void signal_term(int signal_num) 
{
	PyGILState_STATE gstate;
	gstate = PyGILState_Ensure();

	/* Perform Python actions here.  */
	PyObject *game = Game::instance();
	PyObject *game_dict = PyModule_GetDict(game);
	PyObject *run = PyDict_GetItemString(game_dict, "onServerShutdown");

	PyObject_CallObject(run, NULL);
	/* evaluate result */

	/* Release the thread. No Python API allowed beyond this point. */
	PyGILState_Release(gstate);

	/*
	PyInterpreterState * mis;
	PyThreadState * mts,*ts;
	PyEval_InitThreads();
	 PyEval_AcquireLock();
//	mts = PyThreadState_Get();
	//mis = mts->interp;
	//ts = PyThreadState_New(mis); /* stored away somewhere */
	/*
	Note: we don't need to PyEval_AcquireLock, as we already have the lock.

		  Inside the callback:
	*/

	 // PyEval_AcquireLock();
	  //PyThreadState_Swap(ts);
	  /* call python code here */
	/*
	  PyObject *game = Game::instance();
	  PyObject *game_dict = PyModule_GetDict(game);
	  PyObject *run = PyDict_GetItemString(game_dict, "onServerShutdown");

	  PyObject_CallObject(run, NULL);

	  PyThreadState_Swap(NULL);
	  PyEval_ReleaseLock();

	  //Finishing up:

	  PyThreadState_Swap(NULL);
	  PyThreadState_Clear(ts);
	  PyThreadState_Delete(ts);
	  
	  //Py_Finalize();
	  */
	exit(1);
	//Game::gameShutdown(0);
}

GameSignal::GameSignal(void)
{
}


GameSignal::~GameSignal(void)
{
}

void GameSignal::registerSignal(int signal_num, void(*fun)(int)) {
	signal(signal_num, fun);
}