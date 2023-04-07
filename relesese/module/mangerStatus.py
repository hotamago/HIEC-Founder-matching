import os
import json

class MangerStatus():
    def __init__(self, init_data: dict(), loc_file = "config", format_file = "json"):
        self.init_data = init_data
        self.loc_file = loc_file
        self.format_file = format_file
        self.full_path = "{0}.{1}".format(loc_file, format_file)

        self._get()

    def _get(self):
        if not os.path.exists(self.full_path):
            with open(self.full_path, "wt") as f:
                f.write(json.dumps(self.init_data))
            self._data = self.init_data
        else:
            with open(self.full_path, "rt") as f:
                self._data = json.loads(f.read())

    def _set(self):
        with open(self.full_path, "wt") as f:
            f.write(json.dumps(self._data))

    def exists_key(self, key):
        if key in self._data:
            return True
        return False

    def set_value(self, key, value):
        self._data[key] = value

        self._set()

    def set_values(self, dict_pair_key_value):
        for key, value in dict_pair_key_value.items():
            self._data[key] = value
        
        self._set()
    
    def get_value(self, key):
        if not self.exists_key(key):
            ValueError("Value '%s' not found" % (key))
        return self._data[key]
    
    def get_value_or_default(self, key, default = None):
        if not self.exists_key(key):
            return default
        return self._data[key]
    
    def refresh_data(self):
        self._get()