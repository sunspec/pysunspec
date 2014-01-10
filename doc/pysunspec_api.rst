==============
 API Reference
==============

:mod:`sunspec.core` --- SunSpec Core Functionality
==================================================

The core package contains modules that provide the ability to interact with SunSpec devices and encode/decode documents in SunSpec standard formats.
The modules in the core package used to interact with SunSpec devices are organized into the following main functional areas: base SunSpec device/model support, Modbus protocol support, and client device support.

The device module provides objects that map to the SunSpec model definitions within the SunSpec standards.
A device is a collection of SunSpec model definitions that are implemented by a SunSpec compliant device. The device module provides objects for device,
model, block, and point instances as well as objects that support the model, block, and point type definitions.

The modbus package provides protocol support for Modbus TCP, Modbus RTU, and locally defined Modbus maps that can be accessed directly.

The client module extends the basic objects in the device module to provide objects that can be used to access devices using the Modbus protocol objects supplied in the modbus package.

:mod:`sunspec.core.client` --- SunSpec Client classes
=====================================================

.. module:: sunspec.core.client

Classes
-------

.. class:: SunSpecClientDevice

    .. method:: __init__(device_type, slave_id=None, name=None, pathlist=None, baudrate=None, parity=None, ipaddr=None, ipport=None, timeout=None, trace=False)
        
        :param device_type:
             Device type. Possible values: :const:`RTU`, :const:`TCP`, :const:`MAPPED`.

        :param slave_id:
            Modbus slave id.

        :param name:
            For :const:`RTU` devices, the name of the serial port such as 'com4' or '/dev/ttyUSB0'. For :const:`MAPPED` devices, the name of the modbus map file.

        :param pathlist:
            Pathlist object containing alternate paths to support files.

        :param baudrate:
            For :const:`RTU` devices, baud rate such as 9600 or 19200. Defaulted by modbus module to 9600.

        :param parity:
            For :const:`RTU` devices, parity. Possible values:
            :const:`sunspec.core.client.PARITY_NONE`, :const:`sunspec.core.client.PARITY_EVEN`
            Defaulted by modbus module to :const:`PARITY_NONE`.

        :param ipaddr:
            For :const:`TCP` devices, device IP address.

        :param ipport:
            For :const:`TCP` devices, device IP port. Defaulted by modbus module to 502.

        :param timeout:
            Modbus request timeout in seconds. Fractional seconds are permitted such as .5.

        :param trace:
            Enable low level trace.

        :exception SunSpecClientError: Raised for any sunspec module error.

        This class wraps the sunspec.core.ClientDevice class to provide an alternate syntax for scripting. By placing the model (fixed block) points, and
        repeating block points directly on the model and repeating block objects as attributes, the syntax for accessing them is simplified.

        The model and block classes within the device are dynamically generated based on the model type with the appropriate attributes being added during
        creation.

    .. method:: close()

        Release resources associated with the device. Should be called when the device object is no longer in use.

    .. method:: read()

        Read the points for all models in the device from the physical device.

    Attributes:

    .. attribute:: device

        The :const:`sunspec.core.client.ClientDevice` associated with this object.

    .. attribute:: models

        List of models present in the device in the order in which they appear in the device. If there is a single instance
        of the model in the device, the list element is a model object.

        If there are multiple instances of the same model in the list, the list element for that model is a list of
        the models of that type in the order in which they appear in the device with the first element having an index of 1.


.. class:: SunSpecClientModelBase

    .. method:: __init__(model, name):

        :param model:
             The :const:`sunspec.core.device.Model` associated with the model.

        :param name:
             Model name as specified in the model definition.

        :exception SunSpecClientError: Raised for any sunspec module error.

        This class forms the base class of the dynamically generated model classes during SunSpecClientDevice initialization. In
        addition to the attributes listed below, the model (fixed block) points are placed as attributes on the model.

    .. method:: read()

        Read all points in the model from the physical device.

    .. method:: write()

        Write all points that have been modified since the last write operation to the physical device.

    Attributes:

    .. attribute:: model

        The :const:`sunspec.core.device.Model` object associated with the model.

    .. attribute:: name

        Model name as specified in the model definition.

    .. attribute:: repeating

        Repeating block if the model contains one.

    .. attribute:: repeating_name

        Repeating block name.

    .. attribute:: points

        Names of the point attributes added to the model object.

.. class:: SunSpecClientBlockBase

    .. method:: __init__(block, name)

        :param block:
             The :const:`sunspec.core.device.Block` object associated with the block.

        :param name:
             Repeating block name as specified in the model definition.

        This class forms the base class of the dynamically generated repeating block classes during SunSpecClientDevice initialization. In
        addition to the attributes listed below, the repeating block points are placed as attributes on the repeating block.

    Attributes:

    .. attribute:: block

        The :const:`sunspec.core.device.Block` object associated with the block.

    .. attribute:: name

        Block name as specified in the model definition.

    .. attribute:: points

        Names of the point attributes added to the block object.

.. class:: ClientDevice(sunspec.core.device.Device)

    .. method:: __init__(device_type, slave_id=None, name=None, pathlist=None, baudrate=None, parity=None, ipaddr=None, ipport=None, timeout=None, trace=False)

        :param device_type:
             Device type. Possible values: :const:`RTU`, :const:`TCP`, :const:`MAPPED`.

        :param slave_id:
            Modbus slave id.

        :param name:
            For :const:`RTU` devices, the name of the serial port such as 'com4' or '/dev/tty2'. For :const:`MAPPED` devices, the name of the modbus map file.

        :param pathlist:
            Pathlist object containing alternate paths to support files.

        :param baudrate:
            For :const:`RTU` devices, baud rate such as 9600 or 19200. Defaulted by modbus module to 9600.

        :param parity:
            For :const:`RTU` devices, parity. Possible values:
            :const:`PARITY_NONE`, :const:`PARITY_EVEN`
            Defaulted by modbus module to :const:`PARITY_NONE`.

        :param ipaddr:
            For :const:`TCP` devices, device IP address.

        :param ipport:
            For :const:`TCP` devices, device IP port. Defaulted by modbus module to 502.

        :param timeout:
            Modbus request timeout in seconds. Fractional seconds are permitted such as .5.

        :param trace:
            Enable low level trace.

        :exception SunSpecClientError: Raised for any sunspec module error.

        A derived class based on :const:`sunspec.core.device.Device`. It adds Modbus device access capability to the device base class.

    .. method:: read(addr, count)

        :param addr: Starting Modbus address.
        :param count: Register count.
        :return: Byte string containing register contents.

        Read Modbus device registers.

    .. method:: write(addr, data)

        :param addr: Starting Modbus address.
        :param count: Byte string containing register contents.

        Write Modbus device registers.

    .. method:: read_points()

        Read the points for all models in the device from the physical device.

    .. method:: scan()

        Scan all the models of the physical device and create the corresponding model objects within the device object based on the
        SunSpec model definitions.

    Attributes:

    .. attribute:: type

        Device type. Possible values: :const:`RTU`, :const:`TCP`, :const:`MAPPED`.

    .. attribute:: name

        For :const:`RTU` devices, the name of the serial port such as 'com4' or '/dev/tty2'. For :const:`MAPPED` devices, the name of the modbus map file.

    .. attribute:: pathlist

        Pathlist object containing alternate paths to support files.

    .. attribute:: slave_id

        Modbus slave id.

    .. attribute:: modbus_device

        Modbus device object. Object type is based on the device type.

    .. attribute:: retry_count

        Request retry count. Currently not used.

    .. attribute:: base_addr_list

       List of Modbus base addresses to try when scanning a device for the first time.

.. class:: ClientModel(sunspec.core.device.Model)

    .. method:: __init__(dev=None, mid=None, addr=0, mlen=None, index=1)

        :param dev: Device object associated with the model.
        :param mid: Model id.
        :param addr: Starting Modbus address of the model.
        :param mlen: Model length in Modbus registers.
        :param index: Model index.
        :exception SunSpecClientError: Raised for any sunspec module error.

        A derived class based on :const:`sunspec.core.device.Model`. It adds Modbus device access capability to the model base class.

    .. method:: load()

        Create the block and point objects within the model object based on the corresponding SunSpec model definition.

    .. method:: read_points()

        Read all points in the model from the physical device.

    .. method:: write_points()

        Write all points that have been modified since the last write operation to the physical device.

.. class:: ClientBlock(sunspec.core.device.Block)

    .. method:: __init__(model, addr, blen, block_type, index=1)

        :param model: Model object associated with the block.
        :param addr: Starting Modbus address of the block.
        :param blen: Block length in Modbus registers.
        :param block_type: The block type object associated with block in the model definition.
        :param index: Block index.

        A derived class based on :const:`sunspec.core.device.Block`. It adds Modbus device access capability to the block base class.

.. class:: ClientPoint(sunspec.core.device.Point)

    .. method:: __init__(block=None, point_type=None, addr=None, sf_point=None, value=None):

        :param block: Block object associated with the point.
        :param point_type: The point type object associated with point in the model definition.
        :param addr: Starting Modbus address of the point.
        :param sf_point: Point object associated with the point scale factor if present.
        :param value: Point value.
        :exception SunSpecClientError: Raised for any sunspec module error.

        A derived class based on :const:`sunspec.core.device.Point`. It adds Modbus device access capability to the point base class.

    .. method:: write()

    Write the point to the physical device.

Exceptions
----------

.. exception:: SunSpecClientError

    Derived from :const:`sunspec.core.device.SunSpecError`. Raised for any sunspec module error in sunspec.core.client classes.

Constants
---------

*Device Types*

.. data:: RTU
.. data:: TCP
.. data:: MAPPED

*RTU Device Parity*

.. data:: PARITY_NONE
.. data:: PARITY_EVEN

:mod:`sunspec.core.device` --- SunSpec Device classes
=====================================================

.. module:: sunspec.core.device

The device module provides the base SunSpec device functionality. A SunSpec device consists of a set of SunSpec models
which contain blocks and points as specified in the respective SunSpec model definitions.

Classes
-------

.. class:: Device

    .. method:: __init__(addr=suns.SUNS_BASE_ADDR_DEFAULT)

        :param addr: Modbus base address of device.
        :exception SunSpecError: Any error encountered in device processing.

    .. method:: add_model(model)

        :param model: Model object to add to the device.

        Add a model object to the device.

    .. method:: from_pics(element=None, filename=None, pathlist=None):

        :param element: Element Tree device element.
        :param filename: File name of the PICS document.
        :param pathlist: Pathlist object containing alternate paths to the PICS document.

        The PICS information for the device can be either an Element Tree element for a device from a document already being processed
        or the file name of document in the file system. Populates the device based on the elements within the device element.

    .. method:: to_pics(parent, single_repeating=True)

        :param parent: Element Tree element on which to place the device element.
        :param single_repeating: Flag to indicate whether to include a single or all repeating blocks within each model in the PICS document.

        Adds the device and all elements within the device to the parent element. If *single_repeating* is True, only the first repeating block for each
        model is added to the document.

    .. method:: not_equal(device)

        :param device: Device to compare.

        Determines if the specified device instance is not equal based on all the device attribute values including models, blocks and points.
        If not equal, returns a string indicating why the device is not equal. Returns False if the device is equal.

    Attributes:

    .. attribute:: base_addr

        Modbus base address of the device.

    .. attribute:: models_list

        List of model objects present in the device in the order in which they appear in the device.

    .. attribute:: models

        Dictionary of model object lists reperesenting model types present in the device indexed by model id. The elements are model lists to allow more than one
        model of the same model type to be present in the device.

.. class:: Model

    .. method:: __init__(device=None, mid=None, addr=0, mlen=None, index=1)

        :param device: Device associated with the model.
        :param mid: Model id.
        :param addr: Modbus address of the first point in the model.
        :param mlen: Length of the model in Modbus registers.
        :param index: Model instance index for the model type within the device.
        :exception SunSpecError: Any error encountered in device processing.

    .. method:: load(block_class=Block, point_class=Point)

        :param block_class: Block class to use to create block instances.
        :param point_class: Point class to use to create point instances.

        Loads the model instance with blocks and points based on the SunSpec model type definition.

    .. method:: from_pics(element)

        :param element: Element Tree model element.

        Sets the model contents based on an element tree model type element contained in a SunSpec PICS document.

    .. method:: to_pics(parent, single_repeating=True)

        :param parent: Element Tree element on which to place the model element.
        :param single_repeating: Flag to indicate whether to include a single or all repeating blocks within the model in the PICS document.

        Adds the model and all elements within the model to the parent element. If *single_repeating* is True, only the first repeating block
        is added to the document.

    .. method:: not_equal(model)
  
        :param device: Model to compare.

        Determines if the specified model instance is not equal based on all the model attribute values including blocks and points.
        If not equal, returns a string indicating why the model is not equal. Returns False if the model is equal.

    Attributes:

    .. attribute:: device

        Device instance that contains the model instance.

    .. attribute:: id

        Model id. The model id maps to a SunSpec model type definition.

    .. attribute:: index

        Model instance index for the model type within the device. Model instance indexes start at 1 for the first model type instance.

    .. attribute:: model_type

        The :const:`sunspec.core.device.ModelType` instance associated with the model.

    .. attribute:: addr
 
        Modbus address of the first point in the model.

    .. attribute:: len

        Length of the model in Modbus registers.

    .. attribute:: points_list

        List of fixed block non-scale factor points ordered by offset.

    .. attribute:: points

        Dictionary of fixed block non-scale factor points indexed by point id.

    .. attribute:: points_sf

        Dictionary of fixed block scale factor points indexed by point id.

    .. attribute:: blocks

        List of blocks contained in the model instance. Block 0 is the fixed block if present and blocks 1 to n are the
        repeating block instances.

.. class:: Block

    .. method:: __init__(model, addr, blen, block_type, index=1):

        :param model: Model associated with the block.
        :param addr: Modbus address of the first point in the block.
        :param blen: Length of the block in Modbus registers.
        :param block_type: The :const:`sunspec.core.device.BlockType` instance associated with the block.
        :param index: Block instance index for the block type within the model.

    .. method:: from_pics(element)

        :param element: Element Tree model element.

        Sets the block contents based on an element tree model type element contained in a SunSpec PICS document.

    .. method:: to_pics(parent)

        :param parent: Element Tree element on which to place the block element.

        Adds the block and all elements within the block to the parent element.

    .. method:: not_equal(block)
  
        :param device: Block to compare.

        Determines if the specified block instance is not equal based on all the block attribute values including points.
        If not equal, returns a string indicating why the block is not equal. Returns False if the block is equal.

    Attributes:

    .. attribute:: model

        Model associated with the block.

    .. attribute:: block_type

        The :const:`sunspec.core.device.BlockType` instance associated with the block.

    .. attribute:: addr

        Modbus address of the first point in the block.

    .. attribute:: len

        Length of the block in Modbus registers.

    .. attribute:: type

        Block type, either :const:`sunspec.core.suns.SUNS_BLOCK_FIXED` or :const:`sunspec.core.suns.SUNS_BLOCK_REPEATING`.

    .. attribute:: index

        Block instance index for the block type within the model.

    .. attribute:: points_list

        List of non-scale factor points in the block ordered by offset.

    .. attribute:: points

        Dictionary of non-scale factor points in the block indexed by point id.

    .. attribute:: points_sf

        Dictionary of scale factor points int the block indexed by point id.

.. class:: Point

    .. method:: __init__(block=None, point_type=None, addr=None, sf_point=None, value=None)

        :param block: Block associated with the point.
        :param point_type: The :const:`sunspec.core.device.PointType` instance associated with the point.
        :param addr: The Modbus address of the point.
        :param sf_point: Scale factor point associated with the point if present.
        :param value: Initial value for the *value_base* attribute of the point.

    .. method:: from_pics(element)

        :param element: Element Tree model element.

        Sets the block contents based on an element tree model type element contained in a SunSpec PICS document.

    .. method:: to_pics(parent)

        :param parent: Element Tree element on which to place the point element.

        Adds the point to the parent element.

    .. method:: not_equal(point)
  
        :param device: Point to compare.

        Determines if the specified point instance is not equal based on all the point attribute values.
        If not equal, returns a string indicating why the point is not equal. Returns False if the point is equal.

    Attributes:

    .. attribute:: block

        Block associated with the point.

    .. attribute:: point_type

        The :const:`sunspec.core.device.PointType` instance associated with the point.

    .. attribute:: addr

        Modbus address of the point.

    .. attribute:: sf_point

        Scale factor point associated with the point if present.

    .. attribute:: impl

        Indication if the point is implemented. A value of True indicates the point is implmented. Intended to be used for cases when no
        initial value is given for the point but the implementation status is known as in SunSpec PICS documents.

    .. attribute:: value_base

        Value of the point without the point scale factor applied.

    .. attribute:: value_sf

        Scale factor point value.

    .. attribute:: dirty

        Indication if the point has been written to the physical device since the last update of the point. A value of True indicates
        that the point has not been written since the last update.

    .. attribute:: value

        Value of the point with the scale factor applied.

.. class:: ModelType

    .. method:: __init__(mid=None)

        :param mid: Model id that identifies a specific SunSpec model type definition.

    .. method:: from_smdx(element)

        :param element: Element Tree model type element.

        Sets the model type attributes based on an element tree model type element contained in an SMDX model definition.

    .. method:: not_equal(model_type)

        :param model_type: Model type to compare.

        Determines if the specified model type instance is not equal based on all the model type attribute values including blocks and points.
        If not equal, returns a string indicating why the model type is not equal. Returns False if the model type is equal.

    Attributes:

    .. attribute:: id

        Model id that identifies a specific SunSpec model type definition.

    .. attribute:: len

        Length in Modbus registers of the model type as specified in the model definition.

    .. attribute:: label

        Label string as specified in the model definition.

    .. attribute:: description

        Description string as specified in the model definition.

    .. attribute:: notes

        Notes string as specified in the model definition.

    .. attribute:: fixed_block

        Fixed block type as specified in the model definition if present.

    .. attribute:: repeating_block
 
        Repeating block type as specified in the model definition if present.

.. class:: BlockType

    .. method:: __init__(btype=None, blen=0)

        :param btype:
            Block type as specified in the model definition. Valid values are sunspec.core.suns.SUNS_BLOCK_FIXED or sunspec.core.suns.SUNS_BLOCK_REPEATING.
        :param blen: Block length in Modbus registers.


    .. method:: from_smdx(element)

        :param element: Element Tree block type element.

        Sets the block type attributes based on an element tree block type element contained in an SMDX model definition.

    .. method:: not_equal(block_type)

        :param block_type: Block type to compare.

        Determines if the specified block type instance is not equal based on all the block type attribute values including points.
        If not equal, returns a string indicating why the block type is not equal. Returns False if the block type is equal.

    Attributes:

    .. attribute:: type

        Block type as specified in the model definition. Valid values are sunspec.core.suns.SUNS_BLOCK_FIXED or
        sunspec.core.suns.SUNS_BLOCK_REPEATING.

    .. attribute:: len

        Block length in Modbus registers.

    .. attribute:: points_list

        List containing the points in the block in offset order.

    .. attribute:: points

        Dictionary containg the points in the block indexed by the point id.

.. class:: PointType

    .. method:: __init__(pid=None, offset=None, ptype=None, plen=None, mandatory=None, access=None, sf=None)

        :param pid: Point id as specified in the model definition.
        :param offset: Point offset within the block as specified in the model definition.
        :param ptype: Point type as specified in the model definition. Valid values are defined in sunspec.core.suns.SUNS_TYPE_*.
        :param plen: Point length in Modbus registers for points that have a type of 'string'.
        :param mandatory:
            Mandatory indication as specified in the model definition. Valid values are sunspec.core.suns.SUNS_MANDATORY_TRUE or sunspec.core.suns.SUNS_MANDATORY_FALSE.
        :param access:
            Point access setting as specfied in the model definition. Valid values are sunspec.core.suns.SUNS_ACCESS_R or sunspec.core.suns.SUNS_ACCESS_RW.
        :param sf: Id of the scale factor point associated with the point or None if the point does not have a scale factor.

    .. method:: from_smdx(element, strings=False)

        :param element: Element Tree point type element.
        :param strings: Indicates if *element* is a subelement of the 'strings' definintion within the model definition.

        Sets the point attributes based on an element tree point element contained in an SMDX model definition.

    .. method:: not_equal(point_type)

        :param point_type: Point type to compare.

        Determines if the specified point type instance is not equal based on all the point type attribute values. If not equal, returns string
        indicating why the point type is not equal. Returns False if the point type is equal.

    Attributes:

    .. attribute:: id
 
        Point id as specified in the model definition.

    .. attribute:: offset

        Point offset within the block as specified in the model definition.

    .. attribute:: type

        Point type as specified in the model definition. Valid values are defined in sunspec.core.suns.SUNS_TYPE_*.

    .. attribute:: len

        Point length in Modbus registers for points that have a type of 'string'.

    .. attribute:: mandatory
 
        Mandatory indication as specified in the model definition. Valid values are sunspec.core.suns.SUNS_MANDATORY_TRUE or
        sunspec.core.suns.SUNS_MANDATORY_FALSE.

    .. attribute:: access

        Point access setting as specfied in the model definition. Valid values are sunspec.core.suns.SUNS_ACCESS_R or
        sunspec.core.suns.SUNS_ACCESS_RW.

    .. attribute:: sf

        Id of the scale factor point associated with the point or None if the point does not have a scale factor.

    .. attribute:: label

        Label string as specified in the model definition.

    .. attribute:: description
 
        Description string as specified in the model definition.

    .. attribute:: notes

        Notes string as specified in the model definition.

    .. attribute:: value_default

        Default value for a point instance if no value specified.

    .. attribute:: is_impl

        Contains the function to call with the point value as an argument to determine if the point is implemented.

    .. attribute:: data_to

        Contains the function to call to transform a binary data string to the point value.

    .. attribute:: to_data

        Contains the function to call to transform the point value to a binary data string.

    .. attribute:: to_value

        Contains the function to call to transform a point value string into a point value of the type associated with the point.

Exceptions
----------

.. exception:: SunSpecError

    Raised for sunspec.core.device errors.

:mod:`sunspec.core.modbus` --- SunSpec Modbus Package
========================================================

The Modbus package provides standard Modbus support for Modbus RTU, Modbus TCP, and Modbus file mapped client devices.

:mod:`sunspec.core.modbus.client` --- Modbus Client classes
===========================================================

.. module:: sunspec.core.modbus.client

Classes
-------

.. class:: ModbusClientDeviceRTU

    .. method:: __init__(slave_id, name, baudrate=None, parity=None, timeout=None, ctx=None, trace_func=None, max_count=REQ_COUNT_MAX)

        :param slave_id: Modbus slave id.
        :param name: Name of the serial port such as 'com4' or '/dev/ttyUSB0'.
        :param baudrate: Baud rate such as 9600 or 19200. Default is 9600 if not specified.
        :param parity:
            Parity. Possible values: :const:`sunspec.core.modbus.client.PARITY_NONE`, :const:`sunspec.core.modbus.client.PARITY_EVEN`
            Defaulted to :const:`PARITY_NONE`.
        :param timeout: Modbus request timeout in seconds. Fractional seconds are permitted such as .5.
        :param ctx: Context variable to be used by the object creator. Not used by the modbus module.
        :param trace_func: Trace function to use for detailed logging. No detailed logging is perform is a trace function is not supplied.
        :param max_count: Maximum register count for a single Modbus request.
        :exception ModbusClientError: Raised for any general modbus client error.
        :exception ModbusClientTimeoutError: Raised for a modbus client request timeout.
        :exception ModbusClientException: Raised for an exception response to a modbus client request.

        Provides access to a Modbus RTU device.

    .. method:: close()

        Close the device. Called when device is not longer in use.

    .. method:: read(addr, count, op=FUNC_READ_HOLDING)

        :param addr: Starting Modbus address.
        :param count: Read length in Modbus registers.
        :param op: Modbus function code for request.
        :return: Byte string containing register contents.

        Read Modbus device registers.

    .. method:: write(addr, data)

        :param addr: Starting Modbus address.
        :param count: Byte string containing register contents.

        Write Modbus device registers.

    Attributes:

    .. attribute:: slave_id

        Modbus slave id.

    .. attribute:: client

        The :const:`sunspec.core.modbus.client.ModbusClientRTU` instance used for Modbus communication.

    .. attribute:: ctx

        Context variable to be used by the object creator. Not used by the modbus module.

    .. attribute:: trace_func

        Trace function to use for detailed logging.

    .. attribute:: max_count

        Maximum register count for a single Modbus request.

.. class:: ModbusClientDeviceTCP

    .. method:: __init__(slave_id, ipaddr, ipport=502, timeout=2, ctx=None, trace_func=None, max_count=REQ_COUNT_MAX, test=False)

        :param slave_id: Modbus slave id.
        :param ipaddr: IP address string.
        :param ipport: IP port.
        :param timeout: Modbus request timeout in seconds. Fractional seconds are permitted such as .5.
        :param ctx: Context variable to be used by the object creator. Not used by the modbus module.
        :param trace_func: Trace function to use for detailed logging. No detailed logging is perform is a trace function is not supplied.
        :param max_count: Maximum register count for a single Modbus request.
        :param test: Use test socket. If True use the fake socket module for network communications.
        :exception ModbusClientError: Raised for any general modbus client error.
        :exception ModbusClientTimeoutError: Raised for a modbus client request timeout.
        :exception ModbusClientException: Raised for an exception response to a modbus client request.

        Provides access to a Modbus TCP device.

    .. method:: connect(timeout=2)

        :param timeout: Connection timeout in seconds.

        Connect to TCP destination.

    .. method:: disconnect()

        Disconnect from TCP destination.

    .. method:: close()

        Close the device. Called when device is not longer in use.

    .. method:: read(addr, count, op=FUNC_READ_HOLDING)

        :param addr: Starting Modbus address.
        :param count: Read length in Modbus registers.
        :param op: Modbus function code for request.
        :return: Byte string containing register contents.

        Read Modbus device registers. If no connection exists to the destination, one is created and disconnected at the end of the request.

    .. method:: write(addr, data)

        :param addr: Starting Modbus address.
        :param count: Byte string containing register contents.

        Write Modbus device registers. If no connection exists to the destination, one is created and disconnected at the end of the request.

    Attributes:

    .. attribute:: slave_id

        Modbus slave id.

    .. attribute:: ipaddr

        Destination device IP address string.

    .. attribute:: ipport

        Destination device IP port.

    .. attribute:: timeout

        Modbus request timeout in seconds. Fractional seconds are permitted such as .5.

    .. attribute:: ctx

        Context variable to be used by the object creator. Not used by the modbus module.

    .. attribute:: socket

        Socket used for network connection. If no connection active, value is None.

    .. attribute:: trace_func

        Trace function to use for detailed logging.

    .. attribute:: max_count

        Maximum register count for a single Modbus request.

.. class:: ModbusClientDeviceMapped

    .. method:: __init__(slave_id, name, pathlist=None, max_count=None, ctx=None)

        :param slave_id: Modbus slave id.
        :param name: Modbus map file name. Must be in mbmap format.
        :param pathlist: Pathlist object containing alternate paths for modbus map file.
        :param max_count: Maximum register count for a single Modbus request.
        :param ctx: Context variable to be used by the object creator. Not used by the modbus module.
        :exception ModbusClientError: Raised for any general modbus client error.
        :exception ModbusClientTimeoutError: Raised for a modbus client request timeout.
        :exception ModbusClientException: Raised for an exception response to a modbus client request.

        Provides access to a Modbus device implemented as a modbus map (mbmap) formatted file.

    .. method:: close()

        Close the device. Called when device is not longer in use.

    .. method:: read(addr, count, op=FUNC_READ_HOLDING)

        :param addr: Starting Modbus address.
        :param count: Read length in Modbus registers.
        :param op: Modbus function code for request.
        :return: Byte string containing register contents.

        Read Modbus device registers. If no connection exists to the destination, one is created and disconnected at the end of the request.

    .. method:: write(addr, data)

        :param addr: Starting Modbus address.
        :param count: Byte string containing register contents.

        Write Modbus device registers. If no connection exists to the destination, one is created and disconnected at the end of the request.

    Attributes:

    .. attribute:: slave_id

        Modbus slave id.

    .. attribute:: ctx

        Context variable to be used by the object creator. Not used by the modbus module.

    .. attribute:: modbus_map

        The :const:`sunspec.core.modbus.mbmap.ModbusMap` instance associated with the device.

.. class:: ModbusClientRTU

    .. method:: __init__(name='/dev/ttyUSB0', baudrate=9600, parity=None)

        :param name: Name of the serial port such as 'com4' or '/dev/ttyUSB0'.
        :param baudrate: Baud rate such as 9600 or 19200. Default is 9600 if not specified.
        :param parity:
            Parity. Possible values: :const:`sunspec.core.modbus.client.PARITY_NONE`, :const:`sunspec.core.modbus.client.PARITY_EVEN`.
            Defaults to :const:`PARITY_NONE`.
        :exception ModbusClientError: Raised for any general modbus client error.
        :exception ModbusClientTimeoutError: Raised for a modbus client request timeout.
        :exception ModbusClientException: Raised for an exception response to a modbus client request.

        A Modbus RTU client that multiple devices can use to access devices over the same serial interface. Currently, the implementation
        does not support concurent device requests so the support of multiple devices must be single threaded.

    .. method:: open()

        Open the RTU client serial interface.

    .. method:: close()

        Close the RTU client serial interface.

    .. method:: add_device(slave_id, device)

        :param slave_id: Modbus slave id.
        :param device: Device to add to the client.

        Add a device to the RTU client.

    .. method:: remove_device(slave_id)

        :param slave_id: Modbus slave id.

        Remove a device from the RTU client.

    .. method:: read(slave_id, addr, count, op=FUNC_READ_HOLDING, trace_func=None, max_count=REQ_COUNT_MAX)

        :param slave_id: Modbus slave id.
        :param addr: Starting Modbus address.
        :param count: Read length in Modbus registers.
        :param op: Modbus function code for request. Possible values: :const:`FUNC_READ_HOLDING`, :const:`FUNC_READ_INPUT`.
        :param trace_func: Trace function to use for detailed logging. No detailed logging is perform is a trace function is not supplied.
        :param max_count: Maximum register count for a single Modbus request.
        :return: Byte string containing register contents.

    .. method:: write(slave_id, addr, data, trace_func=None, max_count=REQ_COUNT_MAX)

        :param slave_id: Modbus slave id.
        :param addr: Starting Modbus address.
        :param data: Byte string containing register contents.
        :param trace_func: Trace function to use for detailed logging. No detailed logging is perform is a trace function is not supplied.
        :param max_count: Maximum register count for a single Modbus request.

    Attributes:

    .. attribute:: name

        Name of the serial port such as 'com4' or '/dev/ttyUSB0'.

    .. attribute:: baudrate

        Baud rate.

    .. attribute:: parity

        Parity. Possible values: :const:`sunspec.core.modbus.client.PARITY_NONE`, :const:`sunspec.core.modbus.client.PARITY_EVEN`

    .. attribute:: serial

        The pyserial.Serial object used for serial communications.

    .. attribute:: timeout

        Read timeout in seconds. Fractional values are permitted.

    .. attribute:: write_timeout

        Write timeout in seconds. Fractional values are permitted.

    .. attribute:: devices

        List of :const:`sunspec.core.modbus.client.ModbusClientDeviceRTU` devices currently using the client.

Exceptions
----------

.. exception:: ModbusClientError

    Raised for general errors in sunspec.core.modbus.client modules.

.. exception:: ModbusClientTimeout

    Raised for Modbus timeout errors. Derived from :const:`ModbusClientError`.

.. exception:: ModbusClientException

    Raised for Modbus protocol exceptions. Derived from :const:`ModbusClientError`.

Constants
---------

*Parity*

.. data:: PARITY_NONE
.. data:: PARITY_EVEN

*Read Modbus Functions*

.. data:: FUNC_READ_HOLDING
.. data:: FUNC_READ_INPUT

:mod:`sunspec.core.modbus.mbmap` --- Modbus Map classes
========================================================

The mbmap module implements a local Modbus map image. The map supports read and write operations and can be used by Modbus clients
in place of an actual modbus device. The module supports an xml encoding for representing modbus maps as a document.

The xml representation has a root element of *mbmap* that contains a set of *regs* elements representing one or more registers in the map.
Currently only big endian is supported.

Attributes for *mbmap* element:

+-----------+--------------------------------------------+-------------------------------+----------------------+
| Attribute | Description                                | Valid values                  | Default value        |
+===========+============================================+===============================+======================+
| addr      | Base Modbus address                        | Valid modbus address          | 40000                |
+-----------+--------------------------------------------+-------------------------------+----------------------+
| func      | Modbus function associated with the map    | holding, input                | holding              |
+-----------+--------------------------------------------+-------------------------------+----------------------+

Attributes for *regs* element:

+-----------+--------------------------------------------+-------------------------------+----------------------+
| Attribute | Description                                | Valid values                  | Default value        |
+===========+============================================+===============================+======================+
| offset    | Register offset                            | Value with map length         | Next offset          |
+-----------+--------------------------------------------+-------------------------------+----------------------+
| type      | Register(s) type                           | s16, u16, s32, u32, s64, u64, | hexstr               |
|           |                                            | f32, f64, string, hexstr      |                      |
+-----------+--------------------------------------------+-------------------------------+----------------------+
| len       | String length for string type              | Value within map length       | Length of the *regs* |
|           |                                            |                               | element value        |
+-----------+--------------------------------------------+-------------------------------+----------------------+

If the registers are contiguous, offset is optional.

The *hexstr* type is a series of ascii hex characters. Spaces are removed from the string before processing and
can be used to increase readability.

Example::

    <mbmap>
      <!-- common model -->
      <regs type="string" len="2">SunS</regs>
      <regs type="u16">1</regs>
      <regs type="u16">66</regs>
      <regs type="string" len="16">SunSpecTest</regs>
      <regs type="string" len="16">TestInverter-1</regs>
      <regs type="string" len="8">opt_a_b_c</regs>
      <regs type="string" len="8">1.2.3</regs>
      <regs type="string" len="16">sn-123456789</regs>
      <regs type="u16">1</regs>
      <regs type="u16">0</regs>

      <!-- short test model -->
      <regs type="u16">63010</regs>
      <regs type="u16">4</regs>

      <!-- example of hexstr -->
      <regs>00 79 00 1E</regs>
      <regs>0079 001E</regs>

      <!-- end of models -->
      <regs type="u16">0xffff</regs>
      <regs type="u16">0</regs>
    </mbmap>

.. module:: sunspec.core.modbus.mbmap

Classes
-------

.. class:: ModbusMap

    .. method:: __init__(slave_id=None, func=MBMAP_FUNC_HOLDING, base_addr=MBMAP_BASE_ADDR_DEFAULT)

        :param slave_id: Modbus slave id.
        :param func:
            Modbus function string associated with the map. Valid values are: :const:`sunspec.core.modbus.mbmap.MBMAP_FUNC_HOLDING` or
            :const:`sunspec.core.modbus.mbmap.MBMAP_FUNC_INPUT`.
        :param base_addr: Base address of the Modbus map.
        :exception ModbusMapError: Raised for any modbus map error.

    .. method:: from_xml(filename, pathlist=None)

        :param filename: File name of the Modbus map file
        :param pathlist: Pathlist object containing alternate paths to the Modbus map file.

        Load Modbus map from a Modbus map (mbmap) formatted file.

    .. method:: read(addr, count)

        :param addr: Starting Modbus address.
        :param count: Read length in Modbus registers.
        :return: Byte string containing register contents.

        Read Modbus map registers.

    .. method:: write(addr, data)

        :param addr: Starting Modbus address.
        :param count: Byte string containing register contents.

        Write Modbus map registers.

    .. method:: not_equal(mbmap)
    
        Determines if the specified modbus map instance is not equal based on the content of the map.
        If not equal, returns a string indicating why the map is not equal. Returns False if the map is equal.

    Attributes:

    .. attribute:: slave_id

        Modbus slave id.

    .. attribute:: func

        Actual Modbus function associated with the map.

    .. attribute:: base_addr

        Base address of the Modbus map.

    .. attribute:: regs

        List of :const:`sunspec.core.modbus.mbmap.ModbusMapRegs` blocks that comprise the Modbus register map.

.. class:: ModbusMapRegs

    .. method:: __init__(offset, count, data, access=MBMAP_REGS_ACCESS_R)

        :param offset: Register offset into Modbus map.
        :param count: Register count.
        :param data: Byte string containing register data.
        :param access:
            Access for the register block. Valid values are: :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_R` and
            :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_RW`.
        :exception ModbusMapError: Raised for any modbus map error.

    .. method:: read(offset, count)

        :param offset: Register offset into Modbus map.
        :param count: Register count.
        :return: Byte string containing register contents.

        Read Modbus map registers in register block.

    .. method:: write(offset, data)

        :param addr: Register offset into Modbus map.
        :param count: Byte string containing register contents.

        Write Modbus map registers tp register block.

    .. method:: append(offset, count, data, access=MBMAP_REGS_ACCESS_R)

        :param offset: Register offset into Modbus map.
        :param count: Register count.
        :param data: Byte string containing register data.
        :param access:
            Access for the register block. Valid values are: :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_R` and
            :const:`sunspec.core.modbus.mbmap.MBMAP_REGS_ACCESS_RW`.

        Append registers to end of register block.

    .. method:: not_equal(regs)

        Determines if the specified modbus map block instance is not equal based on the content of the map block.
        If not equal, returns a string indicating why the map block is not equal. Returns False if the map block is equal.

    Attributes:

    .. attribute:: offset

        Start register offset of the register block.

    .. attribute:: count

        Register count in the block.

    .. attribute:: data

        Byte string containing data in the register block.

    .. attribute:: access

        Access setting for the block. The access setting is currently not enforced.

Exceptions
----------

.. exception:: ModbusMapError

    Raised for errors in sunspec.core.modbus.mbmap modules.

Constants
---------

*Modbus Map Functions*

.. attribute:: MBMAP_FUNC_INPUT
.. attribute:: MBMAP_FUNC_HOLDING
