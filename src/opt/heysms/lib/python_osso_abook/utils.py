import os
import ctypes

def find_library(name, root=None):
    root = root or "/usr/lib/"
    for dirpath, dirnames, filenames in os.walk(root):
        identifier = filter(lambda x: x.startswith(name), filenames)
        identifier = filter(lambda x: ".so" in x, identifier)
        identifier = filter(lambda x: not os.path.islink(os.path.join(dirpath, x)), identifier)
        if identifier:
            return identifier.pop()
    

identifier = find_library("libglib-2.0")
glib = ctypes.CDLL(identifier)

def glist(addr):
    class _GList(ctypes.Structure):
        _fields_ = [('data', ctypes.c_void_p),
                    ('next', ctypes.c_void_p)]
    l = addr
    while l:
        l = _GList.from_address(l)
        yield l.data
        l = l.next
    glib.g_list_free(addr)
        
def typed_glist(cls, addr):
    for obj in glist(addr):
        yield cls(obj)
        
# ctypes wrapper for pygobject_new(), based on code snippet from
# http://faq.pygtk.org/index.py?req=show&file=faq23.041.htp
class _PyGObject_Functions(ctypes.Structure):
    _fields_ = [
        ('register_class',
            ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p,
            ctypes.c_int, ctypes.py_object, ctypes.py_object)),
        ('register_wrapper',
            ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.py_object)),
        ('register_sinkfunc',
            ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
        ('lookupclass',
            ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_int)),
        ('newgobj',
            ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
    ]
 
class PyGObjectCAPI(object):
    def __init__(self):
        import gobject
        py_obj = ctypes.py_object(gobject._PyGObject_API)
        addr = ctypes.pythonapi.PyCObject_AsVoidPtr(py_obj)
        self._api = _PyGObject_Functions.from_address(addr)
 
    def pygobject_new(self, addr):
        return self._api.newgobj(addr)
        
CAPI = PyGObjectCAPI()

if __name__ == "__main__":
    print find_library("libebook-1.2")
