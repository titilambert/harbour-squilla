import sys
import gobject
from python_osso_abook.addressbook import AddressBook
import gobject
 
if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: %s <phone_number>" % sys.argv[0]
    sys.exit(1)
 
phone_number = sys.argv[1]
 




loop = gobject.MainLoop()
gcontext = loop.get_context()

result = list()
abook = AddressBook.get_default()

def callback(contacts):
    result.extend(contacts)
    loop.quit()

def run():
    abook.find_contacts_for_phone_number(phone_number, True, callback)
abook.find_contacts_for_phone_number(phone_number, True, callback)
gobject.idle_add(run)
loop.run()
print len(result)
print result
import pdb;pdb.set_trace()


