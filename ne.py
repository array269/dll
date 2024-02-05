import ctypes

# Load DLL into memory.

# dpfpddDll = ctypes.WinDLL ("dpfpdd.dll")
dpfpddDll = ctypes.CDLL("dpfpdd.dll")

# Library initialization.
dpfpdd_init = dpfpddDll.dpfpdd_init
dpfpdd_init.restype = ctypes.c_int
result = dpfpdd_init()
print(f"Initialize result: {result}")

class dpfpdd_hw_descr_struct(ctypes.Structure):
    _fields_ = [('vendor_name', ctypes.c_char_p),
                ('product_name', ctypes.c_char_p),
                ('serial_num', ctypes.c_char_p)] 

class dpfpdd_hw_id_struct(ctypes.Structure):
     _fields_ = [('vendor_id', ctypes.c_ushort),
                ('product_id', ctypes.c_ushort)] 

class dpfpdd_ver_info_struct(ctypes.Structure):
    _fields_ = [('major', ctypes.c_int),
                ('minor', ctypes.c_int),
                ('maintenance', ctypes.c_int)] 

class dpfpdd_hw_version_struct(ctypes.Structure):
    _fields_ = [('hw_ver', dpfpdd_ver_info_struct),
                ('fw_ver', dpfpdd_ver_info_struct),
                ('bcd_rev', ctypes.c_ushort)]     

class dpfpdd_dev_info_struct(ctypes.Structure):
    _fields_ = [('size', ctypes.c_uint),
                ('name', ctypes.c_char_p),
                ('descr', dpfpdd_hw_descr_struct),
                ('id', dpfpdd_hw_id_struct),
                ('ver', dpfpdd_hw_version_struct),
                ('modality', ctypes.c_uint),
                ('technology', ctypes.c_uint)] 

dpfpdd_query_devices = dpfpddDll.dpfpdd_query_devices

dpfpdd_query_devices.restype = ctypes.c_int

dpfpdd_query_devices.argtypes = [ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(dpfpdd_dev_info_struct)]

p1 = ctypes.c_uint(10)
p2 = dpfpdd_dev_info_struct()
result = dpfpdd_query_devices(ctypes.byref(p1),ctypes.byref(p2))
print("dpfpdd_query_devices result: " + str(result))
print(f"p1: {p1}")
print(f"p2: {p2}")
print(f"p2.size: {p2.size}")
# print(f"p2.name: {p2.name}")
print(f"p2.descr: {p2.descr}")
print(f"p2.id.vendor_id: {p2.id.vendor_id}")
print(f"p2.ver.hw_ver.major: {p2.ver.hw_ver.major}")
print(f"p2.modality: {p2.modality}")
print(f"p2.technology: {p2.technology}")


# Library release.
dpfpdd_exit = dpfpddDll.dpfpdd_exit
dpfpdd_exit.restype = ctypes.c_int
result = dpfpdd_exit()
print(f"Un Initialize result: {result}")