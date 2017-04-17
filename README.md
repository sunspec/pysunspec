# Overview

The pySunSpec package provides objects and applications that support
interaction with SunSpec compliant devices and documents.  It can be run in
most environments that support Python and is tested on Wndows 7, MAC OS X, and
Ubuntu.

Copyright (c) 2014 SunSpec Alliance ([License](https://github.com/sunspec/pysunspec/blob/master/LICENSE))


# Features
- Provides access to SunSpec Modbus RTU and TCP devices
- High level object model allowing easy device scripting
- Minimal dependencies for core package allowing it to run in more constrained
  Python environments
- Runs on Windows, Mac, and Linux.


# Requirements
- Python 2.4 - 2.7 (2.7 recommended for most uses)
- pySerial


# Installation

The installation instructions are written to utilize a command line. If using
Windows you will want to open a command prompt window for the installation
process. If on a Unix system use terminal and you may need to add `sudo` in
front of the commands if encountering authorization errors.

Note: The installation guide will be showing the commands as if they were run
in a Unix environment. On Windows the left most part of the command will look
different (`C:\>` instead of `$`). Do not type `$` as part of the command.

## Python

If using Unix Python should already be installed whereas Python is not included
in the standard Windows installation. To check to see if Python is installed
type `python` into the command line. If it is installed you should enter a
Python editor. To exit the editor type `quit()`. If successful you should see
the following

```
$ python
Python 2.7.1 (r271:86832, Jul 31 2011, 19:30:53) 
[GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2335.15.00)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>quit()
```

If Python did not show up you can acquire it from the Python Software
Foundation's [download page](http://www.python.org/download). Keep in mind this
repository currently uses Python 2.7 and not any Python 3.X. Accept all the
default settings during the installation.

> ### If using Windows and just downloaded Python you need to set environment variables
> 
> Set the PATH environment variable to include directories that contain Python
> packages and scripts. The environment variable settings are at: Computer >
> System properties > Advanced system settings > Environment Variables.
> 
> In the System variables section add the following to the 'Path' variable (if
> using a version different than 2.7.x, adjust the string)
> 
> ```
> C:\Python27;C:\Python27\Lib\site-packages\;C:\Python27\Scripts\;
> ```
> 
> If you would like to be able to execute Python scripts without specifying the
> '.py' in the script name, you can also add the '.PY' extension to the end of
> the 'PATHEXT' variable.


## pySerial

To install the pySerial package, try using easy_install

```
$ easy_install -U pyserial
```

If easy install is not present on the system download the archive (.tar.gz)
from https://pypi.python.org/pypi/pyserial (Note if on Windows, use the
Windows installer option (pyserial-x.y-win32.exe) instead and move on to the
next section).  Unpack the archive, enter the ``pyserial-x.y`` directory and
run the following 

```
$ python setup.py install
```

## pySunSpec

>If wanting the git repository you have to add the --recursive flag to get the
>submodule to clone as well
>
>```
>$ git clone --recursive https://github.com/sunspec/pysunspec.git
>```

Download the pysunspec archive (.zip) from the [pySunSpec Releases
Page](https://github.com/sunspec/pysunspec/releases).

Unpack the archive, enter the ``pysunspec-x.y`` directory and run

```
$ python setup.py install
```

You can test the installation by opening a Command Prompt window and running
the pysunspec_test.py script. You should see the results of the test execution
with no test failures

```
$ pysunspec_test.py

Test device path: C:\Python27\lib\site-packages\sunspec\core\test\devices

Test device module: total tests: 10  tests run: 10  tests passed: 10  tests failed: 0
Test client module: total tests: 3  tests run: 3  tests passed: 3  tests failed: 0
Test modbus client module: total tests: 4  tests run: 4  tests passed: 4  tests failed: 0
Test modbus mbmap module: total tests: 1  tests run: 1  tests passed: 1  tests failed: 0
Test data module: total tests: 1  tests run: 1  tests passed: 1  tests failed: 0

Total tests run: 19  Total tests passed: 19  Total tests failed: 0

$
```

You should now be ready to use the pySunSpec package.


# Documentation

We are in the process of getting the docs hosted on www.readthedocs.org but in
the meantime they can be found in the /docs/ folder.


# Questions, Bugs, Feature Requests

If you have a question, think you've found a bug or have a feature request
please open an [issue](https://github.com/sunspec/pysunspec/issues) on the
Github Project Page
