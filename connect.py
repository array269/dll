import cffi
import os

ffi = cffi.FFI()

script_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_path,'dpfpdd.h'), "r") as f:
    try:
        ffi.cdef(f.read())
    except Exception as e:
        print(e)

lib = ffi.dlopen('dpfpdd.dll')

chelc = 0