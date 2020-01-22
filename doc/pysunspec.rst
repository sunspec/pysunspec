==========
 Overview
==========

The pySunSpec package provides objects and applications that support interaction with SunSpec compliant devices and documents.
It can be run in most environments that support Python and is tested on Windows 7, macOS, and Ubuntu.

Copyright (c) 2018 SunSpec Alliance


Features
========
- Provides access to SunSpec Modbus RTU and TCP devices
- High level object model allowing easy device scripting
- Minimal dependencies for core package allowing it to run in more constrained Python environments
- Runs on Windows, Mac, and Linux.


Requirements
============
- Python 2.7, 3.5-3.8
- pySerial


Installation
============

Windows
-------

Python
~~~~~~

Python is not included in the standard Windows 7 installation. To check the Python installation, open a Command Promt window
and try to run Python. You should see the Python interactive prompt. Use ^Z <return> to exit Python::

    C:\> python
    Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 

If your Windows environment does not have Python 2.x already installed, install the 32-bit verion of Python using the
Python 2.7.x Windows installers at http://www.python.org/download/. Accept all the default settings during installation.

Setting Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set the PATH environment variable to include directories that contain Python packages and scripts. The environment variable
settings are at: Computer > System properties > Advanced system settings > Environment Variables.

In the System variables section add the following to the 'Path' variable (if using a version different than 2.7.x, adjust the string)::

    C:\Python27;C:\Python27\Lib\site-packages\;C:\Python27\Scripts\;

If you would like to be able to execute Python scripts without specifying the '.py' in the script name, you can also add the '.PY'
extension to the end of the 'PATHEXT' variable.

pySerial
~~~~~~~~

To install the pySerial package, use the Window installer option (pyserial-x.y-win32.exe) at https://pypi.python.org/pypi/pyserial.

pySunSpec
~~~~~~~~~

Download the pysunspec archive (.zip) from .

Unpack the archive, enter the ``pysunspec-x.y`` directory and run::

    C:\> python setup.py install

You can test the installation by opening a Command Prompt window and running the unittest discover command. You should see the results
of the test execution with no test failures::

    C:\> python -m unittest discover -v sunspec

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

    C:\>

You should now be ready to use the pySunSpec package.

Mac/Linux
---------

.. note::

    The following installation steps are performed from a terminal window. If a standard installation is
    performed, sudo (or the equivalent on the system) is necessary to allow update of the system directories.

Python
~~~~~~

Verify Python 2.x is installed. Most current Mac/Linux systems come with Python already installed. To check the Python
installation, open a terminal window and try to run Python. You should see the Python interactive prompt. Use ^D to exit
Python::

    $ python
    Python 2.7.1 (r271:86832, Jul 31 2011, 19:30:53) 
    [GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2335.15.00)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

For more detailed information about using Python in the Mac environment see http://docs.python.org/2/using/mac.html.

pySerial
~~~~~~~~

To install the pySerial package, try using easy_install::

    $ easy_install -U pyserial

If easy install is not present on the system download the archive (.tar.gz) from https://pypi.python.org/pypi/pyserial.
Unpack the archive, enter the ``pyserial-x.y`` directory and run::

    $ python setup.py install

pySunSpec
~~~~~~~~~

Download the pysunspec archive (.zip) from .

Unpack the archive, enter the ``pysunspec-x.y`` directory and run::

    $ python setup.py install

You can test the installation by opening a Command Prompt window and running the unittest discover command. You should see the results
of the test execution with no test failures::

    $ python -m unittest discover -v sunspec

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

    $

You should now be ready to use the pySunSpec package.

Interacting with a SunSpec Device
=================================

The SunSpecClientDevice object is used for high level access to a SunSpec device. It provides the ability to easily read and write all points
within the models that comprise the device. The SunSpecClientDevice object is a wrapper around the ClientDevice object to provide the
easiest syntax for basic operations. For complete access to the device instance and type information, the ClientDevice object can be referenced
within the SunSpecClientDevice object.

The SunSpecClientDevice is populated with dynamically created class objects based on the models found in the device. Point attibutes are added
to the model and repeating blocks based on the points in the respective model definitions. The point attribute names are the same as the point
ids in the model definitions. For points that have associated scale factors, the point value automatically incorporates the value of the scale
factor and the scale factor points do not appear in the points list for the model.

The examples below are shown in interactive mode in the Python interpreter but would typically be performed in a Python script.

Create a device object to access Modbus RTU device at slave id 1 with serial settings of "9600,8,N,1" on serial port 'com6'. The physical device
is scanned and the device object is created based on the SunSpec models found in the device.

    >>> import sunspec.core.client as client
    >>> d = client.SunSpecClientDevice(client.RTU, 1, 'com6')
    >>>

Determine which models are present in the device::

    >>> print d.models
    ['common', 'inverter', 'nameplate', 'settings', 'status', 'controls', 'volt_var']
    >>>

Determine which points are present in a model. The points in the fixed block of a model appear as attributes of the model. Point in the
repeating block appear as attributes of the repeating block instance as descriped in the section on repeating block naming below.

    >>> print d.commmon.points
    ['Mn', 'Md', 'Opt', 'Vr', 'SN', 'DA']
    >>>

View common model contents::

    >>> print d.common
    
    common (1):
    Mn:  SunSpecTest
    Md:  TestInverter-1
    Opt:  opt_a_b_c
    Vr:  1.2.3
    SN:  sn-123456789
    DA:  1

    >>>

The device object mirrors the values in the actual physical device. When the device object is created all the values are read from
the physical device.

To reacquire the values from the physical device, an explicit read operation must be done with a read() operation either on the device or a model within the device. The smallest granularity for a read operation is model to ensure all scale factor values are up to date.

To update the physical device with values that have been set in the device, an explict write() operation must be done on the device or a model within the device. The write operation is performed on the model. Only the fields that have changed in the model are actually written to the
physical device. In general the updates to the device are made in Modbus offset order but this should not be assumed so if value update ordering is
important, write() operations should be performed between object updates to achieve the desired order.

Perform read() to view latest inverter model contents::

    >>> d.inverter.read()
    >>> print d.inverter

    inverter (103):
    A:  12.4
    AphA:  4.1
    AphB:  4.2
    AphC:  4.3
    PhVphA:  240.1
    PhVphB:  240.2
    PhVphC:  240.3
    W:  2970
    Hz:  59.99
    VA:  2978
    VAr:  0.1
    PF:  0.995
    WH:  1234567
    DCA:  10.0
    DCV:  300.1
    DCW:  3001
    TmpCab:  40.1
    TmpSnk:  40.2
    TmpTrns:  40.3
    TmpOt:  40.4
    St:  1

    >>>

If a model contains repeating blocks, the default block name within the model is 'repeating' which along with an index (starting at 1) can
always be used to access the block. If the block has a name specified within the model definition, the name can be also used to access the block as well. The 'repeating_name' attribute of the model contains the alternate name value for the block if one exists. If there is no alternate name, the value of 'repeating_name' is also 'repeating'.

View repeating block name for volt_var model::

    >>> print d.volt_var.repeating_name
    curve
    >>>

View volt_var model contents::

    >>> d.volt_var

    volt_var (126):
    ActCrv:  1
    ModEna:  0
    WinTms:  0
    RvrtTms:  600
    NCrv:  2
    NPt:  4

    curve[1]:
    ActPt:  4
    DeptRef:  2
    V1:  95
    VAr1:  100
    V2:  98
    VAr2:  0
    V3:  102
    VAr3:  0
    V4:  105
    VAr4:  -100
    RmpDecTmm:  0
    RmpIncTmm:  0
    ReadOnly:  0

    curve[2]:
    ActPt:  4
    DeptRef:  2
    V1:  95
    VAr1:  100
    V2:  98
    VAr2:  0
    V3:  102
    VAr3:  0
    V4:  105
    VAr4:  -100
    RmpDecTmm:  0
    RmpIncTmm:  0
    ReadOnly:  0

    >>>

Update a portion of volt_var curve 2 and make active curve::

    >>> d.volt_var.curve[2].V1 = 96
    >>> d.volt_var.curve[2].VAr1 = 100
    >>> d.volt_var.curve[2].V2 = 97
    >>> d.volt_var.curve[2].VAr2 = 0
    >>> d.volt_var.curve.ActCrv = 2
    >>> d.volt_var.write()
    >>>

Enable volt_var curves::

    >>> d.volt_var.ModEna = 1
    >>> d.volt_var.write()
    >>>

The close() method should be called for the device object when it is no longer needed::

    >>> d.close()

