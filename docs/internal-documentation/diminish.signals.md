# diminish.signals package

## Submodules

## diminish.signals.inputSignal module


### class diminish.signals.inputSignal.InputSignal(device, buffer, stepSize, threadName)
Bases: `threading.Thread`


#### \__init__(device, buffer, stepSize, threadName)
This constructor should always be called with keyword arguments. Arguments are:

*group* should be None; reserved for future extension when a ThreadGroup
class is implemented.

*target* is the callable object to be invoked by the run()
method. Defaults to None, meaning nothing is called.

*name* is the thread name. By default, a unique name is constructed of
the form “Thread-N” where N is a small decimal number.

*args* is the argument tuple for the target invocation. Defaults to ().

*kwargs* is a dictionary of keyword arguments for the target
invocation. Defaults to {}.

If a subclass overrides the constructor, it must make sure to invoke
the base class constructor (Thread.__init__()) before doing anything
else to the thread.


#### listener(indata, frames, time, status)

#### run()
Method representing the thread’s activity.

You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.


#### stop()
## diminish.signals.outputSignal module


### class diminish.signals.outputSignal.OutputSignal(device, buffer, stepSize, waitCondition, threadName)
Bases: `threading.Thread`


#### \__init__(device, buffer, stepSize, waitCondition, threadName)
This constructor should always be called with keyword arguments. Arguments are:

*group* should be None; reserved for future extension when a ThreadGroup
class is implemented.

*target* is the callable object to be invoked by the run()
method. Defaults to None, meaning nothing is called.

*name* is the thread name. By default, a unique name is constructed of
the form “Thread-N” where N is a small decimal number.

*args* is the argument tuple for the target invocation. Defaults to ().

*kwargs* is a dictionary of keyword arguments for the target
invocation. Defaults to {}.

If a subclass overrides the constructor, it must make sure to invoke
the base class constructor (Thread.__init__()) before doing anything
else to the thread.


#### listener(outdata, frames, time, status)

#### run()
Method representing the thread’s activity.

You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.


#### stop()
## diminish.signals.targetSignal module


### class diminish.signals.targetSignal.TargetSignal(targetFile, buffer, stepSize, size, threadName)
Bases: `threading.Thread`


#### \__init__(targetFile, buffer, stepSize, size, threadName)
This constructor should always be called with keyword arguments. Arguments are:

*group* should be None; reserved for future extension when a ThreadGroup
class is implemented.

*target* is the callable object to be invoked by the run()
method. Defaults to None, meaning nothing is called.

*name* is the thread name. By default, a unique name is constructed of
the form “Thread-N” where N is a small decimal number.

*args* is the argument tuple for the target invocation. Defaults to ().

*kwargs* is a dictionary of keyword arguments for the target
invocation. Defaults to {}.

If a subclass overrides the constructor, it must make sure to invoke
the base class constructor (Thread.__init__()) before doing anything
else to the thread.


#### run()
Method representing the thread’s activity.

You may override this method in a subclass. The standard run() method
invokes the callable object passed to the object’s constructor as the
target argument, if any, with sequential and keyword arguments taken
from the args and kwargs arguments, respectively.


#### stop()
## Module contents
