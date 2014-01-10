
"""
  Copyright (c) 2014, SunSpec Alliance
  All Rights Reserved

"""

import sunspec.core.suns as suns

PICS_ROOT = 'sunSpecPics'
PICS_ATTR_VERSION = 'v'
PICS_VERSION = '1'
PICS_DATE = 'date'
PICS_MANUFACTURER = 'manufacturer'
PICS_SUBMITTER = 'submitter'
PICS_EMAIL = 'email'
PICS_PHONE = 'phone'
PICS_SLAVE_ID = 'slaveid'
PICS_IP_ADDR = 'ipaddr'
PICS_IP_PORT ='ipport'
PICS_DEVICE = 'device'
PICS_ATTR_BASE_ADDR = 'addr'
PICS_BASE_ADDR_DEFAULT = suns.SUNS_BASE_ADDR_DEFAULT
PICS_MODEL = 'model'
PICS_BLOCK = 'block'
PICS_POINT = 'point'
PICS_ATTR_ID = 'id'
PICS_ATTR_LEN = 'len'
PICS_ATTR_INDEX = 'index'
PICS_ATTR_TYPE = 'type'
PICS_TYPE_FIXED = 'fixed'
PICS_TYPE_REPEATING = 'repeating'
PICS_ATTR_ACCESS = 'access'
PICS_ACCESS_R = 'r'
PICS_ACCESS_RW = 'rw'
PICS_ATTR_IMPLEMENTED = 'impl'
PICS_IMPLEMENTED_FALSE = 'false'
PICS_IMPLEMENTED_TRUE = 'true'

pics_access_types = {
    PICS_ACCESS_R: suns.SUNS_ACCESS_R,
    PICS_ACCESS_RW: suns.SUNS_ACCESS_RW
}

# map PICS block types to SunSpec block types
pics_block_types = {
    PICS_TYPE_FIXED: suns.SUNS_BLOCK_FIXED,
    PICS_TYPE_REPEATING: suns.SUNS_BLOCK_REPEATING
}
