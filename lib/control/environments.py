# control.environments - Controller for cortex Environments resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

from util import globals
from control.resource import ResourceController
from control.exceptions import NotFoundException, MissingException
from rest.client import Client

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
