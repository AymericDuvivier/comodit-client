# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import json, os

from cortex_client.api import collections
from cortex_client.api.exporter import Export
from cortex_client.api.importer import Import
from cortex_client.util import globals
from cortex_client.control.organization_resource import OrganizationResourceController
from cortex_client.control.files import ApplicationFilesController
from cortex_client.control.parameters import ApplicationParametersController
from cortex_client.control.doc import ActionDoc
from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.store_helper import StoreHelper
from cortex_client.control.sync import AppSyncController

class ApplicationsController(OrganizationResourceController):

    _template = "application.json"

    def __init__(self):
        super(ApplicationsController, self).__init__()

        # sub-controllers
        self._register_subcontroller(["files"], ApplicationFilesController())
        self._register_subcontroller(["parameters"], ApplicationParametersController())
        self._register_subcontroller(["sync"], AppSyncController())

        self._doc = "Applications handling."

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)

        helper = StoreHelper(self, "app")
        self._register(["publish"], helper._publish, self._print_resource_completions)
        self._register(["unpublish"], helper._unpublish, self._print_resource_completions)
        self._register(["push"], helper._push, self._print_resource_completions)
        self._register(["pull"], helper._pull, self._print_resource_completions)

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())
        self._register_action_doc(helper._publish_doc())
        self._register_action_doc(helper._unpublish_doc())
        self._register_action_doc(helper._push_doc())
        self._register_action_doc(helper._pull_doc())

    def _get_collection(self, org_name):
        return collections.applications(self._api, org_name)

    def _prune_json_update(self, json_wrapper):
        super(ApplicationsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("organization")
        json_wrapper._del_field("files")
        json_wrapper._del_field("parameters")

    # Export

    def _print_export_completions(self, param_num, argv):
        if param_num < 2:
            self._print_resource_completions(param_num, argv)
        elif param_num == 2:
            self._print_dir_completions()

    def _export(self, argv):
        self._options = globals.options

        app = self._get_resource(argv)

        root_folder = app.get_name()
        if len(argv) > 2:
            root_folder = argv[2]

        export = Export(globals.options.force)
        export.export_application(app, root_folder)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> <app_name> [<output_folder>] [--force]", """
        Export application onto disk. --force option causes existing files to
        be overwritten.""")

    # Import

    def _print_import_completions(self, param_num, argv):
        if param_num < 1:
            self._print_collection_completions(param_num, argv)
        elif param_num == 1:
            self._print_dir_completions()

    def _import(self, argv):
        if len(argv) != 2:
            raise ArgumentException("Wrong number of arguments")

        org = collections.organizations(self._api).get_resource(argv[0])
        imp = Import()
        imp.import_application(org, argv[1])

    def _import_doc(self):
        return ActionDoc("import", "<org_name> <src_folder> [--skip-existing]", """
        Import application from disk. --skip-existing option causes existing resources
        on server to be updated.""")
