import ctypes

DPFPDD_SUCCESS = 0

DPFPDD_QUALITY = ctypes.c_uint
DPFPDD_QUALITY_GOOD = 0
DPFPDD_QUALITY_TIMED_OUT = 1
DPFPDD_QUALITY_CANCELED = (1 << 1)
DPFPDD_QUALITY_NO_FINGER = (1 << 2)
DPFPDD_QUALITY_FAKE_FINGER = (1 << 3)
DPFPDD_QUALITY_FINGER_TOO_LEFT = (1 << 4)
DPFPDD_QUALITY_FINGER_TOO_RIGHT = (1 << 5)
DPFPDD_QUALITY_FINGER_TOO_HIGH = (1 << 6)
DPFPDD_QUALITY_FINGER_TOO_LOW = (1 << 7)
DPFPDD_QUALITY_FINGER_OFF_CENTER = (1 << 8)
DPFPDD_QUALITY_SCAN_SKEWED = (1 << 9)
DPFPDD_QUALITY_SCAN_TOO_SHORT = (1 << 10)
DPFPDD_QUALITY_SCAN_TOO_LONG = (1 << 11)
DPFPDD_QUALITY_SCAN_TOO_SLOW = (1 << 12)
DPFPDD_QUALITY_SCAN_TOO_FAST = (1 << 13)
DPFPDD_QUALITY_SCAN_WRONG_DIRECTION = (1 << 14)
DPFPDD_QUALITY_READER_DIRTY = (1 << 15)

DPFPDD_HW_MODALITY = ctypes.c_uint
DPFPDD_HW_MODALITY_UNKNOWN = 0
DPFPDD_HW_MODALITY_SWIPE = 1
DPFPDD_HW_MODALITY_AREA = 2

DPFPDD_HW_TECHNOLOGY = ctypes.c_uint
DPFPDD_HW_TECHNOLOGY_UNKNOWN = 0
DPFPDD_HW_TECHNOLOGY_OPTICAL = 1
DPFPDD_HW_TECHNOLOGY_CAPACITIVE = 2
DPFPDD_HW_TECHNOLOGY_THERMAL = 3
DPFPDD_HW_TECHNOLOGY_PRESSURE = 4

MAX_STR_LENGTH = 256

MAX_DEVICE_NAME_LENGTH = 1024

_DP_FACILITY = 0x05BA

DPFPDD_STATUS = ctypes.c_uint

class DPFPDD_DEV_STATUS(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("status", ctypes.c_uint),
        ("finger_detected", ctypes.c_int),
        ("data", ctypes.c_char_p)
    ]

class DPFPDD_HW_DESCR(ctypes.Structure):
    _fields_ = [
        ("vendor_name", ctypes.c_char_p),
        ("product_name", ctypes.c_char_p),
        ("serial_num", ctypes.c_char_p)
    ]

class DPFPDD_HW_ID(ctypes.Structure):
    _fields_ = [
        ("vendor_id", ctypes.c_ushort),
        ("product_id", ctypes.c_ushort)
    ]

class DPFPDD_VER_INFO(ctypes.Structure):
    _fields_ = [
        ("major", ctypes.c_int),
        ("minor", ctypes.c_int),
        ("maintenance", ctypes.c_int)
    ]

class DPFPDD_HW_VERSION(ctypes.Structure):
    _fields_ = [
        ("hm_ver", DPFPDD_VER_INFO),
        ("fm_ver", DPFPDD_VER_INFO),
        ("bcd_rev", ctypes.c_ushort)
    ]

class DPFPDD_DEV_INFO(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("name", ctypes.c_char * MAX_DEVICE_NAME_LENGTH),
        ("descr", DPFPDD_HW_DESCR),
        ("id", DPFPDD_HW_ID),
        ("ver", DPFPDD_HW_VERSION),
        ("modality", DPFPDD_HW_MODALITY),
        ("technology", DPFPDD_HW_TECHNOLOGY)
    ]

class DPFPDD_DEV_CAPS(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("can_capture_image", ctypes.c_int),
        ("can_stream_image", ctypes.c_int),
        ("can_extract_features", ctypes.c_int),
        ("can_match", ctypes.c_int),
        ("can_identify", ctypes.c_int),
        ("has_fp_storage", ctypes.c_int),
        ("indicator_type", ctypes.c_uint),
        ("has_pwr_mgmt", ctypes.c_int),
        ("has_calibration", ctypes.c_int),
        ("piv_compliant", ctypes.c_int),
        ("resolution_cnt", ctypes.c_uint),
        ("resolutions", ctypes.c_uint * 1)
    ]

class DPFPDD_IMAGE_INFO(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("width", ctypes.c_uint),
        ("height", ctypes.c_uint),
        ("res", ctypes.c_uint),
        ("bpp", ctypes.c_uint)
   ]

class DPFPDD_CAPTURE_RESULT(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("success", ctypes.c_int),
        ("quality", DPFPDD_QUALITY),
        ("score", ctypes.c_uint),
        ("info", DPFPDD_IMAGE_INFO)
    ]

def DPERROR(err):
    return ctypes.c_int(err | (_DP_FACILITY << 16))

DPFPDD_E_NOT_IMPLEMENTED = DPERROR(0x0a)
DPFPDD_E_FAILURE =  DPERROR(0x0b)
DPFPDD_E_NO_DATA = DPERROR(0x0c)
DPFPDD_E_MORE_DATA = DPERROR(0x0d)
DPFPDD_E_INVALID_PARAMETER = DPERROR(0x14)
DPFPDD_E_INVALID_DEVICE  = DPERROR(0x15)
DPFPDD_E_DEVICE_BUSY = DPERROR(0x1e)
DPFPDD_E_DEVICE_FAILURE = DPERROR(0x1f)

def get_query_devices():
    myDll = ctypes.CDLL("dpfpdd.dll")
    dpfpdd_init = myDll.dpfpdd_init
    dpfpdd_init.restype = ctypes.c_int
    result = dpfpdd_init()
    
    dpfpdd_query_devices = myDll.dpfpdd_query_devices
    dpfpdd_query_devices.restype = ctypes.c_int
    dpfpdd_query_devices.argtypes = [ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(DPFPDD_DEV_INFO)]
    dev_cnt = ctypes.c_uint(10)
    dev_infos = DPFPDD_DEV_INFO(10) #Assuming maximum of 10 devices

    result = dpfpdd_query_devices(ctypes.byref(dev_cnt), ctypes.byref(dev_infos))
    if result == DPFPDD_SUCCESS:
        for i in range(dev_cnt.value):
            dev_info = dev_infos[i]
            print(f"Device {i+1}:")
            print(f"Vendor ID: {dev_info.id.vendor_id}")
            print(f"Product ID: {dev_info.id.product_id}")
            print(f"Name: {dev_info.name.decode('utf-8')}")
            print(f"Vendor: {dev_info.descr.vendor.decode('utf-8')}")
            print(f"Product: {dev_info.descr.product.decode('utf-8')}")
            print(f"Serial Number: {dev_info.descr.serial_number.decode('utf-8')}")
            print(f"Modality: {dev_info.modality}")
            print(f"Technology: {dev_info.technology}")
            print(f"Hardware Version: {dev_info.ver.hm_ver.major}.{dev_info.ver.hm_ver.minor}.{dev_info.ver.hm_ver.maintenance}")
            print(f"Firmware Version: {dev_info.ver.fm_ver.major}.{dev_info.ver.fm_ver.minor}.{dev_info.ver.fm_ver.maintenance}")
            print(f"BCD Revision: {dev_info.ver.bcd_rev}")
            print()
    elif result == DPFPDD_E_MORE_DATA.value:
        print("DPFPDD_E_MORE_DATA")
    elif result == DPFPDD_E_FAILURE.value:
        print("DPFPDD_E_FAILURE")
    elif result == DPFPDD_E_INVALID_PARAMETER.value:
        print("DPFPDD_E_INVALID_PARAMETER")
    elif result == DPFPDD_E_DEVICE_FAILURE.value:
        print("DPFPDD_E_DEVICE_FAILURE")
    elif result == DPFPDD_E_DEVICE_BUSY.value:
        print("DPFPDD_E_DEVICE_BUSY")

    dpfpdd_exit = myDll.dpfpdd_exit
    result = dpfpdd_exit()
def new():
    
    dpfpdd_get_device_status = dpfpdd_get_device_status
    dpfpdd_get_device_status.restype = ctypes.c_int
    dpfpdd_get_device_status.argtypes = [ctypes.c_void_p, ctypes.POINTER(DPFPDD_DEV_STATUS)]
    dev_status = DPFPDD_DEV_STATUS()
    result = dpfpdd_get_device_status(dev, ctypes.pointer(dev_status))


    dpfpdd_get_device_capabilities = dpfpdd_get_device_capabilities
    dpfpdd_get_device_capabilities.restype = ctypes.c_int
    dpfpdd_get_device_capabilities.argtypes = [ctypes.c_void_p, ctypes.POINTER(DPFPDD_DEV_CAPS*10)]
    dev_caps = DPFPDD_DEV_CAPS()
    capsresult = dpfpdd_get_device_capabilities(dev, ctypes.pointer(dev_caps))
    print(f"Device capabilities: {capsresult}")
    print(f"Can capture image: {dev_caps.can_capture_image}")
    print(f"Can stream image: {dev_caps.can_stream_image}")
    print(f"Can extract features: {dev_caps.can_extract_features}")
    print(f"Can match: {dev_caps.can_match}")
    print(f"Can identify: {dev_caps.can_identify}")
    print(f"Has fingerprint storage: {dev_caps.has_fp_storage}")
    print(f"Indicator type: {dev_caps.indicator_type}")
    print(f"Has power management: {dev_caps.has_pwr_mgmt}")
    print(f"Has calibration: {dev_caps.has_calibration}")
    print(f"PIV compliant: {dev_caps.piv_compliant}")
    print(f"Resolution count: {dev_caps.resolution_cnt}")
    print(f"Resolutions: {dev_caps.resolutions}")


def get_version():
    myDll = ctypes.CDLL("dpfpdd.dll")
       
    dpfpdd_version = myDll.dpfpdd_version
    dpfpdd_version.restype = ctypes.c_int
    MEM_SIZE = 1024*1024*128
    ptr = ctypes.cdll.msvcrt.malloc(MEM_SIZE)
    result = dpfpdd_version(ptr)
    if result == DPFPDD_SUCCESS:
        print(f"Version:")
    else:
        print(f"Error: {result}")

    dpfpdd_exit = myDll.dpfpdd_exit
    result = dpfpdd_exit()


class DPFPDD_CAPTURE_PARAM(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("image_fmt", ctypes.c_uint),
        ("image_proc", ctypes.c_uint),
        ("image_res", ctypes.c_uint)
    ]

class DPFPDD_CAPTURE_RESULT(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("success", ctypes.c_int),
        ("quality", DPFPDD_QUALITY),
        ("score", ctypes.c_uint),
        ("info", DPFPDD_IMAGE_INFO)
    ]

def main(): 

    myDll = ctypes.CDLL("dpfpdd.dll")
    dpfpdd_init = myDll.dpfpdd_init
    dpfpdd_init.restype = ctypes.c_int
    result = dpfpdd_init()

    device_id = "05ba&000a&0103{255A0D00-740B-2045-AB16-6AB21DE64CE9}"

    dpfpdd_open = myDll.dpfpdd_open
    dpfpdd_open.restype = ctypes.c_int
    dpfpdd_open.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    device_id_c = ctypes.c_char_p(device_id.encode("ascii")) #device_id.encode("utf-8")

    dev = ctypes.c_void_p()
    open_result = dpfpdd_open(device_id_c, ctypes.pointer(dev))

    dpfpdd_start_stream = myDll.dpfpdd_start_stream
    dpfpdd_start_stream.restype = ctypes.c_int
    dpfpdd_start_stream.argtypes = [ctypes.c_void_p]
    start_result = dpfpdd_start_stream(dev)


    dpfpdd_get_stream_image = myDll.dpfpdd_get_stream_image
    dpfpdd_get_stream_image.restype = ctypes.c_int
    dpfpdd_get_stream_image.argtypes = [ctypes.c_void_p, 
                                        ctypes.POINTER(DPFPDD_CAPTURE_PARAM),
                                        ctypes.POINTER(DPFPDD_CAPTURE_RESULT),
                                        ctypes.POINTER(ctypes.c_uint),
                                        ctypes.c_char_p]
    
    capture_param = DPFPDD_CAPTURE_PARAM()
    capture_result = DPFPDD_CAPTURE_RESULT()
    img_size = ctypes.c_uint(0)
    img = ctypes.c_char_p()

    result = dpfpdd_get_stream_image(dev, ctypes.pointer(capture_param), ctypes.pointer(capture_result), img_size, img)


    close = myDll.dpfpdd_close
    close.restype = ctypes.c_int
    close.argtypes = [ctypes.c_void_p]
    close_result = close(dev)

    dpfpdd_exit = myDll.dpfpdd_exit
    ex_result = dpfpdd_exit()


main()




