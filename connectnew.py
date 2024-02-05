import ctypes

class DPFPDD_VER_INFO(ctypes.Structure):
    _fields_ = [
        ("major", ctypes.c_int),
        ("minor", ctypes.c_int),
        ("maintenance", ctypes.c_int)
    ]

class DPFPDD_VERSION(ctypes.Structure):
    _fields_ = [
        ("size", ctypes.c_uint),
        ("lib_ver", DPFPDD_VER_INFO),
        ("api_ver", DPFPDD_VER_INFO)
    ]

dpfpdd = ctypes.cdll.LoadLibrary("dpfpdd.dll")

dpfpdd.dpfpdd_version.restype = ctypes.c_int

def get_version():
    ver = DPFPDD_VERSION()
    result = dpfpdd.dpfpdd_version(ctypes.byref(ver))
    if result == 0:
        return ver
    else:
        raise Exception("Failed to acquire version information.")

print(get_version())