import ctypes
import ctypes.util
from ctypes import Structure
from evolution import ebook

from utils import find_library, glist, typed_glist

identifier = find_library("libebook-1.2")
libebook = ctypes.CDLL(identifier)

class _andor(Structure):
    _fields_ = [
        ("nqs", ctypes.c_int)
    ]
    
class _not(Structure):
    _fields_ = []
    
class _field_test(Structure):
    _fields_ = [
        ("test", ctypes.c_int),
        ("field_name", ctypes.c_wchar_p),
        ("value", ctypes.c_wchar_p)
    ]
    
class _exist(Structure):
    _fields_ = [
        ("field", ctypes.c_int),
        ("vcard_field", ctypes.c_wchar_p)
    ]
    
class _any_field_contains(Structure):
    _fields_ = [
        ("value", ctypes.c_wchar_p)
    ]

class query(ctypes.Union):
    _fields_ = [
        ("andor", _andor),
        ("not", _not),
        ("field_test", _field_test),
        ("exist", _exist),
        ("any_field_contains", _any_field_contains)
    ]

class EBookQueryStructure(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("ref_count", ctypes.c_int),
        ("query", query)    
    ]    

_andor._fields_.append(("qs", ctypes.POINTER(ctypes.POINTER(EBookQueryStructure))))
_not._fields_.append(("q", ctypes.POINTER(EBookQueryStructure)))


class EBookQuery(object):
    
    @classmethod
    def from_string(cls, string):
        from_string = libebook.e_book_query_from_string
        from_string.argtypes = [ctypes.c_char_p]
        addr = from_string(str(string))
        return cls(addr)
        
    @classmethod
    def field_exists(cls, field_id):
        return cls(libebook.e_book_query_field_exists(int(field_id)))
        
    @classmethod
    def field_test(cls, field_id, test, value):
        field_test = libebook.e_book_query_field_test
        field_test.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
        return cls(field_test(int(field_id), int(test), str(value)))
        
    @classmethod
    def any_field_contains(cls, value):
        any_field_contains = libebook.e_book_query_any_field_contains
        any_field_contains.argtypes = [ctypes.c_char_p]
        return cls(any_field_contains(str(value)))
        
    def __init__(self, addr):
        self.__addr = addr
        
    def __hash__(self):
        return self.__addr
        
    @property
    def _struct(self):
        return EBookQueryStructure.from_address(hash(self))
        
    def to_string(self):
        to_string = libebook.e_book_query_to_string
        to_string.restype = ctypes.c_char_p
        return to_string(hash(self))
        
    def _and(self, *queries):
        _and = libebook.e_book_query_andv
        _and.argtypes = [ctypes.c_long]* (len(queries) + 2)
        queries = [hash(self)] + map(hash, queries) + [0]
        return self.__class__(_and(*queries))
        
    def _or(self, *queries):
        _or = libebook.e_book_query_orv
        _or.argtypes = [ctypes.c_long]* (len(queries) + 2)
        queries = [hash(self)] + map(hash, queries) + [0]
        return self.__class__(_or(*queries))
        
    def _not(self):
        return self.__class__(libebook.e_book_query_not(hash(self)))
        
    def __str__(self):
        return self.to_string()
        
    def __and__(self, other):
        return self._and(other)
        
    def __or__(self, other):
        return self._or(other)
        
    def __invert__(self):
        return self._not()

FIELD_TYPES = {
    # dict of <field_id> : <restype>
    ebook.CONTACT_EMAIL: lambda x: [ctypes.string_at(y) for y in glist(x)],
    103: lambda x: [ctypes.string_at(y) for y in glist(x)], #virtual icq contacts field
    118: lambda x: [ctypes.string_at(y) for y in glist(x)], #virtual phone field



}
