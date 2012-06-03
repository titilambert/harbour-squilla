import gobject
import ctypes

from libosso_abook import osso_abook, \
    OssoABookWaitableCallback, OssoABookContactPredicate
from enums import OssoABookAggregatorState, EnumResult
from utils import typed_glist, CAPI
from libebook import FIELD_TYPES
 
class Contact(gobject.GObject):
    
    def __init__(self, OssoABookContact):
        super(Contact, self).__init__()
        self.__contact = OssoABookContact
        self.__roster_contacts = list(self.get_roster_contacts())
        
    def get_property(self, name):
        id = self.field_id(name)
        if id is None:
            raise AttributeError
        return self.get(id)
        
    def get_properties(self, *names):
        return tuple(self.get_property(name) for name in names)
        
    def set_property(self, name, value):
        raise NotImplementedError("all properties are readonly atm")
    
    @property
    def _data(self):
        return self.__contact
        
    def get_persistent_uid(self):
        contact_get_persistent_uid = osso_abook.osso_abook_contact_get_persistent_uid
        contact_get_persistent_uid.restype = ctypes.c_char_p
        result = contact_get_persistent_uid(self.__contact)
        return result
        
    def get_name(self):
        get_name = osso_abook.osso_abook_contact_get_name
        get_name.restype = ctypes.c_char_p
        result = get_name(self.__contact)
        return result
        
    def get(self, field_id):
        get = osso_abook.e_contact_get
        get.argtypes = [ctypes.c_int, ctypes.c_int]
        if field_id in FIELD_TYPES:
            get.restype = FIELD_TYPES[field_id]
        else:
            get.restype = ctypes.c_char_p
        result = get(self.__contact, int(field_id))
        return result
        
    def get_all(self, field_id):
        results = list()
        for contact in [self] + self.__roster_contacts:
            result = contact.get(field_id)
            if result is not None:
                if isinstance(result, list):
                    for x in result:
                        results.append(x)
                else:
                    results.append(result)
        if len(results) == 0:
            return None
        elif len(results) == 1:
            return results.pop()
        else:
            return results
        
    @staticmethod
    def field_name(field_id):
        """ name of a field/attribute """
        field_name = osso_abook.e_contact_field_name
        field_name.restype = ctypes.c_char_p
        return field_name(int(field_id))
        
    @staticmethod
    def pretty_name(field_id):
        """ userreadable field identifier """
        pretty_name = osso_abook.e_contact_pretty_name
        pretty_name.restype = ctypes.c_char_p
        return pretty_name(int(field_id))
        
    @staticmethod
    def field_id(field_name):
        """ id = Contact.field_id(Contact.field_name(id)) """
        field_id = osso_abook.e_contact_field_id
        field_id.argtypes = [ctypes.c_char_p]
        return field_id(str(field_name)) or None
        
    def is_roster_contact(self):
        return bool(osso_abook.osso_abook_contact_is_roster_contact(self.__contact))
        
    def has_roster_contacts(self):
        return bool(osso_abook.osso_abook_contact_has_roster_contacts(self.__contact))
        
    def get_roster_contacts(self):
        get_roster_contacts = osso_abook.osso_abook_contact_get_roster_contacts
        get_roster_contacts.restype = lambda x: typed_glist(Contact, x)
        return get_roster_contacts(self.__contact)
        
    def get_photo(self):
        c_obj = osso_abook.osso_abook_contact_get_photo(self.__contact)
        return CAPI.pygobject_new(c_obj)
        

class AddressBook(gobject.GObject):
    
    @classmethod
    def get_default(cls):
        aggregator = osso_abook.osso_abook_aggregator_get_default(0)
        return cls(aggregator)
        
    def __init__(self, aggregator):
        super(AddressBook, self).__init__()
        self.__aggregator = aggregator
        
    def get_state(self):
        get_state = osso_abook.osso_abook_aggregator_get_state
        get_state.restype = lambda x: EnumResult(OssoABookAggregatorState, x-1)
        return get_state(self.__aggregator)
        
    def lookup(self, uid, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            aggregator_lookup = osso_abook.osso_abook_aggregator_lookup
            aggregator_lookup.restype = lambda x: typed_glist(Contact, x)
            result = aggregator_lookup(aggregator, uid)
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def resolve_master_contacts(self, contact, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            aggregator_resolve_master_contacts = osso_abook.osso_abook_aggregator_resolve_master_contacts
            aggregator_resolve_master_contacts.restype = lambda x: typed_glist(Contact, x)
            result = aggregator_resolve_master_contacts(aggregator, contact._data)
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def list_master_contacts(self, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            list_master_contacts = osso_abook.osso_abook_aggregator_list_master_contacts
            list_master_contacts.restype = lambda x: typed_glist(Contact, x)
            result = list_master_contacts(aggregator)
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def list_roster_contacts(self, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            list_roster_contacts = osso_abook.osso_abook_aggregator_list_roster_contacts
            list_roster_contacts.restype = lambda x: typed_glist(Contact, x)
            result = list_roster_contacts(aggregator)
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def get_master_contact_count(self, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            get_master_contact_count = osso_abook.osso_abook_aggregator_get_master_contact_count
            result = get_master_contact_count(aggregator)
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def find_contacts_full(self, predicate, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            find_contacts_full = osso_abook.osso_abook_aggregator_find_contacts_full
            find_contacts_full.restype = lambda x: typed_glist(Contact, x)
            
            cb_predicate = OssoABookContactPredicate(lambda c: predicate(Contact(c)))
            
            result = find_contacts_full(aggregator, cb_predicate)
            OssoABookWaitableCallback.unregister(cb_proto)
            OssoABookContactPredicate.unregister(cb_predicate)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def find_contacts(self, equery, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        # FIXME: it's somehow not working, all queries return an empty result set
        
        def func(aggregator, error, data):
            find_contacts = osso_abook.osso_abook_aggregator_find_contacts
            find_contacts.restype = lambda x: typed_glist(Contact, x)
            
            result = find_contacts(aggregator, hash(equery))
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def find_contacts_for_phone_number(self, phone_number, fuzzy_match, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        
        def func(aggregator, error, data):
            find_contacts = osso_abook.osso_abook_aggregator_find_contacts_for_phone_number
            find_contacts.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
            find_contacts.restype = lambda x: typed_glist(Contact, x)
            
            result = find_contacts(aggregator, str(phone_number), bool(fuzzy_match))
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
        
    def find_contacts_for_im_contact(self, username, account, callback, *user_data):
        """ callback gets a generator of contacts as only argument """
        # FIXME: it's not working and McAccount is not implemented
        if account is not None:
            raise NotImplementedError("account is not implemented")
        
        def func(aggregator, error, data):
            find_contacts = osso_abook.osso_abook_aggregator_find_contacts_for_im_contact
            find_contacts.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
            find_contacts.restype = lambda x: typed_glist(Contact, x)
            
            result = find_contacts(aggregator, str(username), 0)
            OssoABookWaitableCallback.unregister(cb_proto)
            callback(result, *user_data)
        
        # Keep prototype object reference so it is not destroyed
        cb_proto = OssoABookWaitableCallback(func)
        osso_abook.osso_abook_waitable_call_when_ready(self.__aggregator, cb_proto, 0, 0)
