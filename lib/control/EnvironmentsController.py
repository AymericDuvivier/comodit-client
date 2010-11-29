'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.ResourceController import ResourceController
from control.Exceptions import NotFoundException, MissingException
from rest.Client import Client
from util import globals

class EnvironmentsController(ResourceController):

    _resource = "environments"

    def __init__(self):
        super(EnvironmentsController, self ).__init__()
        
    def _list(self, argv):
        options = globals.options
    
        # Validate input parameters
        if options.uuid:
            uuid = options.uuid
        elif options.path:
            uuid = self._resolv(options.path)
            if not uuid: raise NotFoundException(uuid)
        else:
            raise MissingException("You must provide a valid organization UUID (with --uuid) or path (--path)")
        
        self._parameters = {"organizationId":uuid}
        
        super(EnvironmentsController, self)._list(argv)    
        
        
    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/organization/" + path)
        if result.has_key('uuid') : return result['uuid']
        
    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else:
            print "Name:", item['name']
            print "UUUID:", item['uuid']
            if item.has_key('description'):
                print "Description:", item['description']
            if item.has_key('settings'):
                print "Settings:"
                for setting in item['settings']:
                    print "    %-30s: %s" % (setting['key'], setting['value'])
