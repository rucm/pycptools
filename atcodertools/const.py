import configparser
import sys
import re


class _const:
    class ConstError(object):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError('Can\'t rebind const ({})'.format(name))

        self.__dict__[name] = value

    def setup(self):
        inifile = configparser.ConfigParser().read('config.ini', 'utf-8')

sys.modules[__name__] = _const()
