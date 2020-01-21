# pySunSpec

The pySunSpec package provides objects and applications that support
interaction with SunSpec compliant devices and documents.  It can be run in
most environments that support Python and is tested on Windows 7, Mac OS X, and
Ubuntu.

Copyright (c) 2018 SunSpec Alliance
([License](https://github.com/sunspec/pysunspec/blob/master/LICENSE))

[![Build Status](https://travis-ci.org/sunspec/pysunspec.svg?branch=master)](https://travis-ci.org/sunspec/pysunspec)


# Features

- Provides access to SunSpec Modbus RTU and TCP devices
- High level object model allowing easy device scripting
- Minimal dependencies for core package allowing it to run in more constrained
  Python environments
- Runs on Windows, Mac, and Linux


# Requirements

- Python 2.7, 3.3-3.6
- pySerial


# Installation


## Python

Since this is a Python library you will need Python installed both to run your
code and this library.  Supported Python versions are noted above.  Unless
there is a strong reason not to, it is recommended to use the current Python 3.
The CPython interpreter from [python.org](python.org) is commonly used.
The `#python` community support channel on the Freenode IRC network is usually
quite active and has many knowledgeable and helpful users that can assist with
general Python issues.

Recent versions of the CPython Windows installer offer the option of adding
the Python installation to the system path.  If you are not familiar with this
it is likely a good option to select.  It allows you to run Python from a
shell without having to type the full directory path to Python.  If this option
is not present you can add the paths manually as below.

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


## pySunSpec

When installing from source you need to be sure to have the models available as
well as the pySunSpec source.  The models repository is referenced in the
`.gitmodules` file which allows for it to be included with an initial clone.

```
git clone --recursive https://github.com/sunspec/pysunspec.git
```

If a non-recursive clone was done, the models can be retreived using the
`git submodules` command from within your pySunSpec repository clone.

```
git submodule update --init
```

Python libraries should generally be installed before use.  This reduces issues
relating to paths and dependency on the value of the current working directory.
It is strongly recommended that you work in an isolated environment such as
can be created by `venv` or `virtualenv` (see [bit.ly/py-env](bit.ly/py-env)).
pySunSpec can be installed per the
[package installation tutorial](https://packaging.python.org/tutorials/installing-packages/)
which also discusses virtual environments.


## Dependencies

Depending on which installation method you follow you may need to separately
install the pySerial library that pySunSpec depends on.  This is the case if
you get an error such as `ImportError: No module named 'serial'` when trying
to use the pySunSpec code.  pySerial is available as a Python package from
[PyPi](https://pypi.python.org/pypi/pyserial) and as source from
[GitHub](https://github.com/pyserial/pyserial) as both a Git repository and
a .zip download.


## Verifying the pySunSpec Installation

You can test the installation by opening a Command Prompt window and running
the `unittest discover` command. You should see the results of the test execution
with no test failures.  Depending on how you chose to install Python and
pySunSpec (adding Python to the path, using a virtualenv, etc) you may need
to adjust the `python` portion of the command.

Command:
```
python -m unittest discover -v sunspec
```
Expected result:
```
test_client_device (core.test.test_client.TestClientDevice) ... ok
test_sunspec_client_device_1 (core.test.test_client.TestClientDevice) ... ok
test_sunspec_client_device_3 (core.test.test_client.TestClientDevice) ... ok
test_data (core.test.test_data.TestData) ... ok
test_device_blocktype_not_equal (core.test.test_device.TestDevice) ... ok
test_device_common_len_65 (core.test.test_device.TestDevice) ... ok
test_device_constant_sf (core.test.test_device.TestDevice) ... ok
test_device_from_pics (core.test.test_device.TestDevice) ... ok
test_device_models_smdx (core.test.test_device.TestDevice) ... ok
test_device_modeltype (core.test.test_device.TestDevice) ... ok
test_device_modeltype_not_equal (core.test.test_device.TestDevice) ... ok
test_device_pointtype (core.test.test_device.TestDevice) ... ok
test_device_pointtype_not_equal (core.test.test_device.TestDevice) ... ok
test_device_to_pics (core.test.test_device.TestDevice) ... ok
test_device_value_get (core.test.test_device.TestDevice) ... ok
test_device_value_set (core.test.test_device.TestDevice) ... ok
test_modbus_client_device_rtu_read (core.test.test_modbus_client.TestModbusClient) ... ok
test_modbus_client_device_rtu_write (core.test.test_modbus_client.TestModbusClient) ... ok
test_modbus_client_device_tcp_read (core.test.test_modbus_client.TestModbusClient) ... ok
test_modbus_client_device_tcp_write (core.test.test_modbus_client.TestModbusClient) ... ok
test_modbus_mbmap_from_xml_element (core.test.test_modbus_mbmap.TestModbusMap) ... ok
test_modbus_mbmap_from_xml_file (core.test.test_modbus_mbmap.TestModbusMap) ... ok

----------------------------------------------------------------------
Ran 22 tests in 0.634s

OK
```

You should now be ready to use the pySunSpec package.


# Documentation

The documentation can be found on the [Read the
Docs](https://pysunspec.readthedocs.io/en/latest/) site.


# Questions, Bugs, Feature Requests

If you have a question, think you've found a bug or have a feature request
please open an [issue](https://github.com/sunspec/pysunspec/issues) on the
Github Project Page.
