# control.applications - Controller for cortex Applications resources.
# coding: utf-8
# 
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior 
# authorization from Guardis.

import json

from util import globals
from control.resource import ResourceController
from control.exceptions import ControllerException
from rest.client import Client

class ApplicationsController(ResourceController):

    _resource = "applications"

    def __init__(self):
        super(ApplicationsController, self ).__init__()
        
    def _update(self, args):
        options = globals.options
                  
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
                uuid = item.get("uuid")
        elif options.json:
            item = json.loads(options.json)
            uuid = item.get("uuid")
        else:
            raise ControllerException("Updating an application is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + uuid, item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else: 
            print "Name:", item['name']
            if item.has_key('description'): print "Description:", item['description']
            print "UUID:", item['uuid']
            if item.has_key('packages'):
                print "Packages:"
                for p in item.get('packages'):
                    print "   ", p                 
            if item.has_key('parameters'):
                print "Parameters:"
                for p in item.get('parameters'):
                    print "   ", p.get('key')


    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/application/" + path)
        if result.has_key('uuid') : return result['uuid']            