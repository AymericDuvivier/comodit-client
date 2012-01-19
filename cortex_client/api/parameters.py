from cortex_client.api.resource import Resource

class Parameter(Resource):
    """
    A template's parameter. A parameter is reprensented by a key, a default value
    and a name. A version is also associated to the parameter by the server.
    """
    def __init__(self, collection, json_data = None):
        super(Parameter, self).__init__(collection, json_data)

    def get_key(self):
        """
        Provides parameter's key.
        @return: The key
        @rtype: String
        """
        return self._get_field("key")

    def set_key(self, key):
        """
        Sets parameter's key.
        @param key: The key
        @type key: String
        """
        return self._set_field("key", key)

    def get_value(self):
        """
        Provides parameter's default value.
        @return: The default value
        @rtype: String
        """
        return self._get_field("value")

    def set_value(self, value):
        """
        Sets parameter's default value.
        @param value: The default value
        @type value: String
        """
        return self._set_field("value", value)

    def get_name(self):
        """
        Provides parameter's name.
        @return: The name
        @rtype: String
        """
        return self._get_field("name")

    def set_name(self, name):
        """
        Sets parameter's name.
        @param name: The name
        @type name: String
        """
        return self._set_field("name", name)

    def get_description(self):
        return self._get_field("description")

    def set_description(self, description):
        return self._set_field("description", description)

    def get_version(self):
        """
        Provides parameter's version number.
        @return: The version number
        @rtype: Integer
        """
        return int(self._get_field("version"))

    def _show(self, indent = 0):
        """
        Prints parameter's state to standard output in a user-friendly way.
        
        @param indent: The number of spaces to put in front of each displayed
        line.
        @type indent: Integer
        """
        print " "*indent, "Name:", self.get_name()
        print " "*indent, "Description:", self.get_description()
        print " "*indent, "Key:", self.get_key()
        print " "*indent, "Default value:", self.get_value()


class ParameterFactory(object):
    def __init__(self, collection = None):
        self._collection = collection

    """
    File parameter factory.
    
    @see: L{Parameter}
    @see: L{cortex_client.util.json_wrapper.JsonWrapper._get_list_field}
    """
    def new_object(self, json_data):
        """
        Instantiates a L{Parameter} object using given state.
        
        @param json_data: A quasi-JSON representation of a Package instance's state.
        @type json_data: String, dict or list
        
        @return: A parameter
        @rtype: L{Parameter}
        """
        return Parameter(self._collection, json_data)
