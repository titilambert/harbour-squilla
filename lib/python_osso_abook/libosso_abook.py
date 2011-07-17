import osso
import sys
import ctypes
import gtk

from utils import find_library

def init_osso_abook():
    osso_ctx = osso.Context("test_abook", "0.1")
    identifier = find_library("libosso-abook-1.0")
    osso_abook = ctypes.CDLL(identifier)
    argv_type = ctypes.c_char_p * len(sys.argv)
    argv = argv_type(*sys.argv)
    argc = ctypes.c_int(len(sys.argv))
    osso_abook.osso_abook_init(ctypes.byref(argc), ctypes.byref(argv), hash(osso_ctx))
    return osso_abook
        
osso_abook = init_osso_abook()

WaitableCallback_cache = list()

class WaitableCallback(object):
    
    def __init__(self, return_type, *arg_types):
        self._def = ctypes.CFUNCTYPE(return_type, *arg_types)
        
    def __call__(self, func):
        func = self._def(func)
        WaitableCallback_cache.append(func)
        return func
        
    def unregister(self, func):
        WaitableCallback_cache.remove(func)
    
    
OssoABookWaitableCallback = WaitableCallback(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
OssoABookContactPredicate = WaitableCallback(ctypes.c_int, ctypes.c_void_p)
