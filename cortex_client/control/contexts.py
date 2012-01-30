# control.applications - Controller for cortex Applications resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from cortex_client.control.exceptions import ArgumentException
from cortex_client.control.resource import ResourceController
from cortex_client.control.settings import ApplicationContextSettingsController, \
    PlatformContextSettingsController, DistributionContextSettingsController
from cortex_client.control.doc import ActionDoc

class AbstractContextController(ResourceController):
    def __init__(self):
        super(AbstractContextController, self).__init__()

        # actions
        self._register(["render-file"], self._render_file, self._print_render_file_completions)
        self._unregister(["update"])

        self._update_action_doc_params("list", "<org_name> <env_name> <host_name>")
        self._update_action_doc_params("show", "<org_name> <env_name> <host_name> <name>")
        self._update_action_doc_params("add", "<org_name> <env_name> <host_name>")
        self._update_action_doc_params("delete", "<org_name> <env_name> <host_name> <name>")

        self._register_action_doc(self._render_file_doc())

    def _get_environments(self, argv):
        org = self._api.organizations().get_resource(argv[0])
        return org.environments()

    def _get_hosts(self, argv):
        env = self._get_environments(argv).get_resource(argv[1])
        return env.hosts()

    def _get_host(self, argv):
        return self._get_hosts(argv).get_resource(argv[2])


class ApplicationContextController(AbstractContextController):

    _template = "application_context.json"

    def __init__(self):
        super(ApplicationContextController, self).__init__()

        # subcontroller
        self._register_subcontroller(["settings"], ApplicationContextSettingsController())

        # actions
        self._register(["install"], self._install, self._print_install_completions)
        self._register(["uninstall"], self._uninstall, self._print_resource_completions)

        # 'install' and 'uninstall' are aliases for 'add' and 'delete'
        self._unregister(["add", "delete"])

        self._doc = "Application contexts handling."
        self._register_action_doc(self._install_doc())
        self._register_action_doc(self._uninstall_doc())

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        return host.applications()

    def _complete_template(self, argv, template_json):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments");
        template_json["application"] = argv[3]

    def _get_name_argument(self, argv):
        if len(argv) < 4:
            raise ArgumentException("Wrong number of arguments");

        return argv[3]

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            self._print_identifiers(host.applications())

    def _print_install_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            self._print_identifiers(org.applications())

    def _print_uninstall_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)
        elif len(argv) > 2 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            self._print_identifiers(host.applications())

    def _print_render_file_completions(self, param_num, argv):
        if param_num < 4:
            self._print_uninstall_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            org = self._api.organizations().get_resource(argv[0])
            app = org.applications().get_resource(argv[3])
            self._print_identifiers(app.files())

    def _install(self, argv):
        self._add(argv)

    def _install_doc(self):
        return ActionDoc("install", "<org_name> <env_name> <host_name> <app_name>", """
        Install an application on host.""")

    def _uninstall(self, argv):
        self._delete(argv)

    def _uninstall_doc(self):
        return ActionDoc("uninstall", "<org_name> <env_name> <host_name> <app_name>", """
        Uninstall an application from host.""")

    def _print_file_completions(self, param_num, argv):
        if param_num < 4:
            self._print_resource_completions(param_num, argv)
        elif len(argv) > 3 and param_num == 4:
            org = self._api.organizations().get_resource(argv[0])
            app = org.applications().get_resource(argv[3])
            app_files = app.get_files()
            for f in app_files:
                self._print_escaped_name(f.get_name())

    def _render_file(self, argv):
        if len(argv) != 5:
            raise ArgumentException("Wrong number of arguments");

        host = self._get_host(argv)
        app_name = argv[3]
        file_name = argv[4]

        print host.render_app_file(app_name, file_name).read()

    def _render_file_doc(self):
        return ActionDoc("render-file", "<org_name> <env_name> <host_name> <app_name> <file_name>", """
        Render an application's file.""")


class PlatformContextController(AbstractContextController):

    _template = "platform_context.json"

    def __init__(self):
        super(PlatformContextController, self).__init__()

        # subcontroller
        self._register_subcontroller(["settings"], PlatformContextSettingsController())

        self._unregister(["update", "list"])

        self._doc = "Distribution contexts handling."

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        return host.platform()

    def _get_name_argument(self, argv):
        return ""

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)

    def _print_render_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_resource_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            plat = org.platforms().get_resource(host.get_platform())
            self._print_identifiers(plat.files())

    def _render_file(self, argv):
        if len(argv) != 4:
            raise ArgumentException("Wrong number of arguments");

        host = self._get_host(argv)
        file_name = argv[3]

        print host.render_plat_file(file_name).read()

    def _render_file_doc(self):
        return ActionDoc("render-file", "<org_name> <env_name> <host_name> <file_name>", """
        Render a platform's file.""")

class DistributionContextController(AbstractContextController):

    _template = "distribution_context.json"

    def __init__(self):
        super(DistributionContextController, self).__init__()

        # subcontroller
        self._register_subcontroller(["settings"], DistributionContextSettingsController())

        self._unregister(["update", "list"])

        self._doc = "Distribution contexts handling."

    def get_collection(self, argv):
        if len(argv) < 3:
            raise ArgumentException("Wrong number of arguments");

        org = self._api.organizations().get_resource(argv[0])
        env = org.environments().get_resource(argv[1])
        host = env.hosts().get_resource(argv[2])
        return host.distribution()

    def _get_name_argument(self, argv):
        return ""

    def _print_collection_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self._api.organizations())
        elif len(argv) > 0 and param_num == 1:
            self._print_identifiers(self._get_environments(argv))
        elif len(argv) > 1 and param_num == 2:
            self._print_identifiers(self._get_hosts(argv))

    def _print_resource_completions(self, param_num, argv):
        if param_num < 3:
            self._print_collection_completions(param_num, argv)

    def _print_render_file_completions(self, param_num, argv):
        if param_num < 3:
            self._print_resource_completions(param_num, argv)
        elif len(argv) > 0 and param_num == 3:
            org = self._api.organizations().get_resource(argv[0])
            env = org.environments().get_resource(argv[1])
            host = env.hosts().get_resource(argv[2])
            dist = org.distributions().get_resource(host.get_distribution())
            self._print_identifiers(dist.files())

    def _render_file(self, argv):
        if len(argv) != 4:
            raise ArgumentException("Wrong number of arguments");

        host = self._get_host(argv)
        file_name = argv[3]

        print host.render_dist_file(file_name).read()

    def _render_file_doc(self):
        return ActionDoc("render-file", "<org_name> <env_name> <host_name> <file_name>", """
        Render a distribution's file.""")
